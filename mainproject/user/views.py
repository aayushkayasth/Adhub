from django.shortcuts import render,redirect
from django.http import HttpResponse
from user.models import *
from django.urls import reverse
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.http import FileResponse
import os
from django.conf import settings
from datetime import datetime
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import hmac
import hashlib
from datetime import timedelta
# Create your views here.

def register(request):
    if request.POST.get("btnregc"):
        u=user()
        u.name=request.POST.get("txtname")
        u.username=request.POST.get("txtuname")
        u.password=request.POST.get("txtpass")
        u.emailid=request.POST.get("txtemail")
        u.gender=request.POST.get("gender")
        u.contact=request.POST.get("contact")
        u.cityid=city.objects.filter(cityid=request.POST.get("city")).first()
        if request.FILES.get("fup"):
            u.profilepic=request.FILES["fup"]
        # u.identity=request.POST.get("identity")
        u.save()
        return redirect(login)
    
    if request.POST.get("btnrega"):
        a=advertiser()
        a.name=request.POST.get("txtaname")
        a.advertisername=request.POST.get("txtadname")
        a.password=request.POST.get("txtpwd")
        a.emailid=request.POST.get("txtmail")
        a.gender=request.POST.get("gen")
        a.contact=request.POST.get("txtcontact")
        a.cityid=city.objects.filter(cityid=request.POST.get("txtcity")).first()
        if request.FILES.get("fups"):
            a.profilepic=request.FILES["fups"]
        a.save()
        return redirect(login)
    return render(request,"register.html",{"cities":city.objects.all()})

def home(request):
    # if request.session.get("uname")==None:
    #     return redirect(login)
    # if request.session.get("type")=="C":
    #     type=0
    # else:
    #     type=1
    # print(type)
    # print(request.session.get("uid"))
    
    temp={
        "proj":project.objects.order_by('projectid')[0:3],
        "adv":advertiser.objects.order_by('advertiserid')[0:4],
        "cat":subcategory.objects.all(),
        
    }
    return render(request,"home.html",temp)

def adv(request):
    # if request.session.get("uname")==None:
    #     return redirect(login)
    if request.session.get("uname")==None:
        return redirect(login)
    if request.session.get("type")=="C":
        type=0
    else:
        type=1
    print(type)
    print(request.session.get("uid"))
    nfs=notification.objects.filter(userid=request.session.get("uid"),userType=type).all()
    
    
    temp={
        "adv":advertiser.objects.filter(advertiserid=request.session.get('uid')).first(),
        "user":user.objects.all(),
        "proj":project.objects.all(),
        "notifications":nfs,
        "review":review.objects.filter(advertiserid=request.session.get('uid')).all(),
        "range":range(1,6)
    }
    return render(request,"advProfile.html",temp)

def adv2(request):
    if request.session.get("uname")==None:
        return redirect(login)
    id=request.GET.get('aid')
    if request.POST.get('btnrev'):
        r=review()
        r.review=request.POST.get('txtrev')
        r.rating=request.POST.get('rating')
        r.userid=user.objects.filter(userid=request.session.get('uid')).first()
        r.advertiserid=advertiser.objects.filter(advertiserid=id).first()
        r.save()
    temp={
        "review":review.objects.filter(advertiserid=id).all(),
        "adv":advertiser.objects.filter(advertiserid=id).first(),
        "range":range(1,6)
    }
    return render(request,"advProfile2.html",temp)

def login(request):
    msg={}
    if request.POST.get('btnlogin'):
        if request.POST.get('type')=="Client":
            u=user.objects.filter(username=request.POST.get("txtuname"),password=request.POST.get("txtpass")).first()
            if u==None:
                msg["error"]="Invalid Username and password"
            else:
                request.session["uname"]=u.username
                request.session["uid"]=u.userid
                request.session["fup"]=u.profilepic.url
                request.session["type"]="C"
                return redirect(home)
        else:
            u=advertiser.objects.filter(advertisername=request.POST.get("txtuname"),password=request.POST.get("txtpass")).first()
            if u==None:
                msg["error"]="Invalid Username and password"
            else:
                request.session["uname"]=u.advertisername
                request.session["uid"]=u.advertiserid
                request.session["fup"]=u.profilepic.url
                request.session["type"]="A"
                return redirect(home)
    return render(request,"login.html",msg)

def logout(request):
    del request.session["uname"]
    del request.session["uid"]
    del request.session["fup"]

    return redirect(login)

def postproject(request):
    today = datetime.now().date()
    max_date = today + timedelta(days=365)
    temp={
        "category":category.objects.all(),
        "subcategory":subcategory.objects.all(),
        "advertiser":advertiser.objects.all(),
        "cities":city.objects.all()
    }
    if request.POST.get("btnadd"):
        start_date=request.POST.get("bidstart")
        end_date=request.POST.get("bidend")

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = None  # Handle case where the date is not valid

        if start_date or end_date:
            if start_date < today:
                temp['error_message'] = "start date cannot be in the past."
            elif end_date < today:
                temp['error_message'] = "end date cannot be in the past."
            else:
                p=project()
                p.bname=request.POST.get("txtbname")
                p.title=request.POST.get("txttitle")
                p.budget=request.POST.get("txtbudget")
                p.categoryid=category.objects.filter(categoryid=request.POST.get("txtcategory")).first()
                p.subcategoryid=subcategory.objects.filter(subcategoryid=request.POST.get("txtsubcategory")).first()
                p.cityid=city.objects.filter(cityid=request.POST.get("txtCity")).first()
                p.userid=user.objects.filter(userid=request.session.get('uid')).first()
                p.bidstartdate=start_date
                p.bidenddate=end_date
                p.description=request.POST.get("txtdes")
                p.image=request.FILES["fup"]
                p.save()
                return redirect(displayproject)
    
    
    return render(request,"postproject.html",temp) 

def displayproject(request):
    if request.session.get("uname") is None:
        return redirect(login)

    user_type = request.session.get("type")
    user_id = request.session.get("uid")

    if user_type == "C":
        # If client, show only their own projects
        uid = user.objects.filter(userid=user_id).first()
        proj = project.objects.filter(userid=uid)
    elif user_type == "A":
        # If advertiser, show all projects except their own
        u = advertiser.objects.filter(advertiserid=user_id).first()
        proj = project.objects.exclude(advertiserid=u)
    else:
        # For other user types (e.g. admin or future roles), show all projects
        proj = project.objects.all()

    # Count bids per project
    for p in proj:
        p.bids = projectbid.objects.filter(projectid=p).count()

    # Handle search/filter (only for advertisers)
    if user_type == "A" and request.method == "POST":
        if request.POST.get("btnser"):
            if request.POST.get("subcat"):
                proj = proj.filter(subcategoryid=request.POST.get("subcat"))

            if request.POST.get("city"):
                proj = proj.filter(cityid=request.POST.get("city"))

            if request.POST.get("txtmin"):
                proj = proj.filter(budget__gte=request.POST.get("txtmin"))

            if request.POST.get("txtmax"):
                proj = proj.filter(budget__lte=request.POST.get("txtmax"))

        # Optional chat message (possibly misplaced here)
        if request.POST.get("btnSend"):
            m = chat()
            m.receiverid = request.POST.get("receiverid")  # Fix: define 'id' properly
            m.senderid = user_id
            m.message = request.POST.get("txtMessage")
            m.save()

    context = {
        "projects": proj,
        "total": proj.count(),
        "category": category.objects.all(),
        "subcategory": subcategory.objects.all(),
        "city": city.objects.all(),
        "state": state.objects.all()
    }

    return render(request, "displayproject.html", context)


def projectdetails(request):
    if request.session.get("uname")==None:
            return redirect(login)
    id=request.GET.get('pid')
    p=project.objects.filter(projectid=id).first()
    p.views=p.views+1
    u=advertiser.objects.filter(advertiserid=request.session.get('uid')).first()
    l=like.objects.filter(advertiserid=u,projectid=id).first()
    if l==None:
        isLiked=True
    else:
        isLiked=False
    p.save()
    u=advertiser.objects.filter(advertiserid=request.session["uid"]).first()
    if request.POST.get("placeBid"):
        bid=projectbid()
        bid.bidamount=request.POST.get("txtamount")
        bid.description=request.POST.get("txtdesc")
        bid.projectid=p
        bid.userid=p.userid
        bid.advertiserid=u 
        bid.save()

        notify(p.userid.userid,
            "%s bidded on your project %s"%(u.advertisername,p.title),0)

    currentBid=projectbid.objects.filter(projectid=p,advertiserid=u).first()
    if currentBid ==None:
        hasBidded=False
    else:
        hasBidded=True
    
    p.bids=len(projectbid.objects.filter(projectid=p).all())
    likes=like.objects.all()
    print("------------")
    print(likes)
    print("------------")

    temp={
            "projects":p,
            "disProj":project.objects.filter(userid=request.session.get('uid')).all(),
            "hasBidded":hasBidded,
            "bids":projectbid.objects.filter(projectid=p).all(),
            "userprojects":project.objects.filter(userid=user.objects.filter(userid=request.session.get("uid")).first()).count(),
            "likes":likes,
            "isLiked":isLiked,
            "review":review.objects.all(),
            "range":range(1,6),
            "razorpay_key":"rzp_test_YwEnmHKCrVzx4i"
         }

    return render(request,"projectdetails.html",temp)

def editprofile(request):
    id=request.session["uid"]
    u=user.objects.filter(userid=id).first()
    if request.POST.get("updatebtn"):
        u.name=request.POST.get("txtname")
        u.username=request.POST.get("txtuname")
        u.password=request.POST.get("txtpass")
        u.emailid=request.POST.get("txtemail")
        u.gender=request.POST.get("gender")
        u.contact=request.POST.get("contact")
        u.cityid=city.objects.filter(cityid=request.POST.get("city")).first()
        if request.FILES.get("fup"):
            u.profilepic=request.FILES["fup"]

        u.save()
        request.session["uname"]=u.username
        request.session["fup"]=u.profilepic.url
        return redirect(home)
    return render(request,"editprofile.html",{"userdata":u,"cities":city.objects.all()})

def editprofile2(request):
    id=request.session["uid"]
    a=advertiser.objects.filter(advertiserid=id).first()
    if request.POST.get("updatebtns"):
        a.name=request.POST.get("txtaname")
        a.advertisername=request.POST.get("txtadname")
        a.password=request.POST.get("txtpwd")
        a.emailid=request.POST.get("txtmail")
        a.gender=request.POST.get("gen")
        a.contact=request.POST.get("txtcontact")
        a.cityid=city.objects.filter(cityid=request.POST.get("city")).first()
        if request.FILES.get("fups"):
            a.profilepic=request.FILES["fups"]

        a.save()
        request.session["uname"]=a.advertisername
        request.session["fups"]=a.profilepic.url
        return redirect(home)
    return render(request,"editprofile2.html",{"addata":a,"cities":city.objects.all()})

def myprojects(request):
    id=request.GET.get('uid')
    if request.session.get("uname")==None:
        return redirect(login)
    temp={
        "projects":project.objects.filter(userid=request.session.get("uid")).all()

    }
    return render(request,"myproject.html",temp)

def projectLike(request):
    # uid=request.session["uid"]
    # temp={
    #     "likes":like.objects.filter(userid=uid).all()
    # }
    # return render(request,"likeproject.html",temp)

    if request.session.get("uname")==None:
        return redirect(login)
    temp={
        "project":project.objects.all(),
        "likes":like.objects.filter(advertiserid=request.session["uid"])
    }
    return render(request,"likeproject.html",temp)

def likeProject(request):
    l=like()
    l.advertiserid=advertiser.objects.filter(advertiserid=request.session["uid"]).first()
    l.projectid=project.objects.filter(projectid=request.GET.get("pid")).first()
    l.save()
    params={"pid":request.GET.get("pid")}
    url=reverse(projectdetails)
    qs=urlencode(params)
    url=f"{url}?{qs}" 
    return HttpResponseRedirect(url)

def unlikeProject(request):
    advertiserid=advertiser.objects.filter(advertiserid=request.session["uid"]).first()
    projectid=project.objects.filter(projectid=request.GET.get("pid")).first()
    
    l=like.objects.filter(advertiserid=advertiserid,projectid=projectid).first()
    
    l.delete()
    params={"pid":request.GET.get("pid")}
    url=reverse(projectdetails)
    qs=urlencode(params)
    url=f"{url}?{qs}"
    return HttpResponseRedirect(url)

def myprofile(request):
    if request.session.get("uname")==None:
        return redirect(login)
    id=request.session.get("uid")
    u=user.objects.filter(userid=id).first()
   
    temp={
        "user":user.objects.filter(userid=request.session.get("uid")).first(),
        "project":project.objects.filter(userid=id).all(),
        # "postproject":postproject.objects.all()
        
    }
    return render(request,"myprofile.html",temp)

def myprofile2(request):
    if request.session.get("uname")==None:
        return redirect(login)
    id=request.GET.get("uid")
    u=user.objects.filter(userid=id).first()
   
    temp={
        "user":user.objects.filter(userid=id).first(),
        "project":project.objects.filter(userid=id).all(),
        # "postproject":postproject.objects.all()
        
    }
    return render(request,"myprofile.html",temp)

def mybids(request):
    id=request.GET.get('uid')
    if request.session.get("uname")==None:
        return redirect(login)
    u=advertiser.objects.filter(advertiserid=request.session.get("uid")).first()
    mybids=projectbid.objects.filter(advertiserid=u).all()
    temp={
        "mybids":mybids

    }
    return render(request,"mybids.html",temp)

def delBid(request):
    pid=request.GET.get('pid')
    p=projectbid.objects.filter(projectbidid=pid).first()

    p.delete()
    return redirect(mybids)

def delpro(request):
    id=request.GET.get("pid")
    d=project.objects.filter(projectid=id)
    d.delete()
    return redirect(myprofile)

def about(request):
    return render(request,"about.html")

def forgetpass(request):
    msg={}
    if request.POST.get('btnfor'):
        
        u=user.objects.filter(emailid=request.POST.get("txtemaill")).first()
        if u==None:
            msg["error"]="Invalid email"
        else:
            u.password=request.POST.get('txtpwd')
            u.save()   
            return redirect(login)
    return render(request,"forgetpass.html",msg)

def projectinfo(request):
    cid=request.GET.get('cid')
    temp={
        "projects":project.objects.filter(subcategoryid=cid).all()
    }
    
    return render(request,'projectinfo.html',temp)
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_order(request):
    if request.method == "POST":
        print(request.POST.get("amount"))

        amount = int(request.POST.get("amount")) * 100  # Convert to paisa
        id=request.POST.get("order_id")
        print(id)
        bid=projectbid.objects.filter(projectbidid=id).first()
        bid.status=1
        #bid.projectid.status=1
        #bid.projectid.advertiserid=bid.advertiserid
        bid.save()
        p=project.objects.filter(projectid=bid.projectid.projectid).first()
        p.status=1
        p.advertiserid=bid.advertiserid
        p.save()

        # b.status=3
        # notify(
        #     b.carid.userid.userid,
        #     "%s has made a payment and confimed the booking for your car %s"%(b.userid.username,b.carid.title)
        # )
        #b.save()
        # Create order
        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1",
        }
        notify(p.advertiserid.advertiserid,
            "%s project has been assigned to you. Keep up the good work."%(p.bname),1)
        
        order = razorpay_client.order.create(order_data)
        
        return JsonResponse(order)

    return JsonResponse({"error": "Invalid request"}, status=400)
@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = request.POST
        client_signature = data.get("razorpay_signature")
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            f"{data.get('razorpay_order_id')}|{data.get('razorpay_payment_id')}".encode(),
            hashlib.sha256
        ).hexdigest()

        if client_signature == generated_signature:
            return JsonResponse({"status": "Payment Successful"})

    return JsonResponse({"status": "Payment Failed"}, status=400)
def success(request):
    return render(request,"success.html")

def notify(id,msg,type):
    n=notification()
    n.userid=id
    n.msg=msg
    n.userType=type
    n.save()

def loadsubcat(request):
    id=request.GET.get("cid")
    
    temp={
        "subcats":subcategory.objects.filter(categoryid=category.objects.filter(categoryid=id).first()).all()
    }
    return render(request,"subcat.html",temp)

def loadsubcats2(request):
    id=request.GET.get("cid")
    
    temp={
        "subcats2":subcategory.objects.filter(categoryid=category.objects.filter(categoryid=id).first()).all()
    }
    return render(request,"subcat2.html",temp)

def loadsubcats3(request):
    id=request.GET.get("sid")
    
    temp={
        "subcats":city.objects.filter(stateid=state.objects.filter(stateid=id).first()).all()
    }
    return render(request,"subcat3.html",temp)
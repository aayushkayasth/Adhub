from django.shortcuts import render,redirect
from django.http import HttpResponse
from user.models import *
from django.urls import reverse
from urllib.parse import urlencode
from django.http import HttpResponseRedirect

# Create your views here.
def dashboard(request):
    if request.session.get('aname') == None:
        return redirect(login)
    
    projects=project.objects.all()
    totalproject=projects.count()

    totuser=user.objects.all().count()
    totadv=advertiser.objects.all().count()
    totbid=projectbid.objects.all().count()
    content={
        "project":projects,
        "totproj":totalproject,
        "totusers":totuser,
        "totadv":totadv,
        "totbid":totbid
    }

    return render(request,"dashboard.html",content)
def login(request):
    msg={}
    if request.POST.get('btnadv'):
        
        a=adminLog.objects.filter(email=request.POST.get("txtemail"),password=request.POST.get("txtpwd")).first()
        if a==None:
            msg["error"]="Invalid Username and password"
        else:
            request.session["aname"]=a.aname
            request.session["aid"]=a.aid
            return redirect(dashboard)
        
    return render(request,"adminLogin.html",msg)
def adminprofile(request):
    temp={
        "admin":adminLog.objects.all()
    }
    return render(request,"adminProfile.html",temp)
def updState(request):
    id=request.GET.get('sid')
    s=state.objects.filter(stateid=id).first()
    if request.POST.get('btnupd'):
        s.statename=request.POST.get('txtsname')
        

        s.save()
        return redirect(displayState)
    temp={
        "stateData":s
    }
    return render(request,"updState.html",temp) 
def displayState(request):
    id=request.GET.get('sid')
    if request.POST.get('btnins'):
        s=state()
        s.statename=request.POST.get('txtcname')
        s.save()
    s=state.objects.filter(stateid=id)
    s.delete()
    temp={
        "sta":state.objects.all()
    }
    return render(request,"displayState.html",temp)   

def updCity(request):
    id=request.GET.get('cid')
    c=city.objects.filter(cityid=id).first()
    if request.POST.get('btnupd'):
        c.cityname=request.POST.get('txtcname')
        c.stateid=state.objects.filter(stateid=request.POST.get('state')).first()

        c.save()
        return redirect(displayCity)
    temp={
        "state":state.objects.all(),
        "cityData":c
    }
    return render(request,"updCity.html",temp) 
   
def displayCity(request):
    id=request.GET.get('cid')
    if request.POST.get('btnins'):
        c=city()
        c.cityname=request.POST.get('txtcname')
        c.stateid=state.objects.filter(stateid=request.POST.get('state')).first()

        c.save()
    c=city.objects.filter(cityid=id)
    c.delete()

    temp={
        "ct":city.objects.all(),
        "st":state.objects.all()
    }
    return render(request,"displayCity.html",temp)


def updcategory(request):
    id=request.GET.get('cid')
    c=category.objects.filter(categoryid=id).first()
    if request.POST.get('btnupd'):
        c.categoryid=request.POST.get('catid')
        c.categoryname=request.POST.get('catname')
        c.save()
        return redirect(displayCategory)
    temp={
        "catData":c
    }
    return render(request,"updcategory.html",temp)


def displayCategory(request):
    id=request.GET.get('cid')
    if request.POST.get('btnins'):
        c=category()
        c.categoryname=request.POST.get('catname')
        c.save()
    c=category.objects.filter(categoryid=id)
    c.delete()
    temp={
        "cat":category.objects.all()
    }
    return render(request,"displayCategory.html",temp)


def updsubcategory(request):
    id=request.GET.get('sid')
    s=subcategory.objects.filter(subcategoryid=id).first()
    if request.POST.get('btnupd'):
        s.subcategoryid=request.POST.get('scaid')
        s.subcategoryname=request.POST.get('subcatname')
        s.categoryid=category.objects.filter(categoryid=request.POST.get('state')).first()
        s.save()
        return redirect(displaySubcategory)
    temp={
        "category":category.objects.all(),
        "subData":s
    }
    return render(request,"updsubcategory.html",temp)  
def displaySubcategory(request):
    id=request.GET.get('sid')
    if request.POST.get('btnins'):
        s=subcategory()
        s.subcategoryname=request.POST.get('subname')
        s.categoryid=category.objects.filter(categoryid=request.POST.get('categoryname')).first()

        s.save()
    c=subcategory.objects.filter(subcategoryid=id)
    c.delete()
    temp={
        "sc":subcategory.objects.all(),
        "cat":category.objects.all()
    }
    return render(request,"displaySubcategory.html",temp)

def displayUser(request):
    temp={
        "us":user.objects.all()
    }
    return render(request,"displayUser.html",temp)

def displayAdvertiser(request):
    temp={
        "adver":advertiser.objects.all()
    }
    return render(request,"displayAdvertiser.html",temp)

def Projects(request):
    temp={
        "pro":project.objects.all()
    }
    return render(request,"Projects.html",temp)

def displayProjectSubcategory(request):
    temp={
        "prosub":projectsubcategory.objects.all()
    }
    return render(request,"displayProjectSubcategory.html",temp)

def displayProjectbid(request):
    temp={
        "probid":projectbid.objects.all()
    }
    return render(request,"displayProjectbid.html",temp)


def displayReview(request):
    temp={
        "view":review.objects.all()
    }
    return render(request,"displayReview.html",temp)

def displayLike(request):
    temp={
        "lik":like.objects.all()
    }
    return render(request,"displayLike.html",temp)
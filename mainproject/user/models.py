from django.db import models

class state(models.Model):
    stateid=models.AutoField(primary_key=True)
    statename=models.TextField(max_length=50,null=False)

    def __str__(self):
        return self.statename
class adminLog(models.Model):
    aid=models.AutoField(primary_key=True)
    aname=models.TextField(max_length=50,null=False)
    email=models.TextField(max_length=50,null=False)
    password=models.TextField(max_length=50,null=False)


    def __str__(self):
        return self.aname


class city(models.Model):
    cityid=models.AutoField(primary_key=True)
    cityname=models.TextField(max_length=50,null=False)
    stateid=models.ForeignKey(state,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.cityname 
    
class category(models.Model):
    categoryid=models.AutoField(primary_key=True)
    categoryname=models.TextField(max_length=50,null=False)

    def __str__(self):
        return self.categoryname 

class subcategory(models.Model):
    subcategoryid=models.AutoField(primary_key=True)
    subcategoryname=models.TextField(max_length=50,null=False)
    categoryid=models.ForeignKey(category,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.subcategoryname
    
class user(models.Model):
    userid=models.AutoField(primary_key=True)
    name=models.TextField(max_length=50,null=False)
    username=models.TextField(max_length=50,null=False)
    password=models.TextField(max_length=50,null=False)
    emailid=models.TextField(max_length=50,null=False)
    gender=models.TextField(max_length=50,null=False)
    cityid=models.ForeignKey(city,on_delete=models.CASCADE,null=True)
    contact=models.TextField(max_length=50,null=False)
    profilepic=models.ImageField(upload_to='images/',default="images/default.png")
    createdDt=models.DateField(auto_now=True)
    # identity=models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    
class advertiser(models.Model):
    advertiserid=models.AutoField(primary_key=True)
    name=models.TextField(max_length=50,null=False)
    advertisername=models.TextField(null=False,max_length=50)
    password=models.TextField(null=False,max_length=50)
    emailid=models.TextField(null=False,max_length=50)
    gender=models.TextField(null=False,max_length=50)
    cityid=models.ForeignKey(city,on_delete=models.CASCADE,null=True)
    contact=models.TextField(max_length=50)
    profilepic=models.ImageField(upload_to='images/')
    isverified=models.IntegerField(null=False,default=0)
    website=models.TextField(null=True,max_length=50)
    instagramlink=models.TextField(null=True,max_length=50)
    facebooklink=models.TextField(null=True,max_length=50)
    linkeidlink=models.TextField(null=True,max_length=50)
    registrationdate=models.TimeField(auto_now=True)

    def __str__(self):
        return self.advertisername
    
class project(models.Model):
    projectid=models.AutoField(primary_key=True)
    bname=models.TextField(max_length=50,default='false')
    title=models.TextField(max_length=50)
    budget=models.IntegerField(null=False)
    categoryid=models.ForeignKey(category, on_delete=models.CASCADE)
    subcategoryid=models.ForeignKey(subcategory, on_delete=models.CASCADE)
    createddate=models.DateTimeField( auto_now=True)
    userid=models.ForeignKey(user, on_delete=models.CASCADE)
    cityid=models.ForeignKey(city, on_delete=models.CASCADE)
    advertiserid=models.ForeignKey(advertiser, on_delete=models.CASCADE,null=True)
    bidstartdate=models.DateTimeField( auto_now=False, auto_now_add=False)
    bidenddate=models.DateTimeField(auto_now=False, auto_now_add=False)
    description=models.TextField(max_length=10000)
    image=models.ImageField(upload_to='images/',default="images/default.png")
    views=models.IntegerField(default=0)
    status=models.IntegerField(default=0)
    def __str__(self):
     return self.bname

    
class projectsubcategory(models.Model):
    projectsubcategoryid=models.AutoField(primary_key=True)
    projectid=models.ForeignKey(project, on_delete=models.CASCADE,null=True)
    subcategoryid=models.ForeignKey(subcategory, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.projectsubcategoryid)

class saveproject(models.Model):
    saveprojectid=models.AutoField(primary_key=True)
    projectid=models.ForeignKey(project, on_delete=models.CASCADE,null=True)
    advertiserid=models.ForeignKey(advertiser, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.saveprojectid)
    
class projectbid(models.Model):
    projectbidid=models.AutoField(primary_key=True)
    projectid=models.ForeignKey(project,null=False,on_delete=models.CASCADE)
    bidamount=models.IntegerField(null=False)
    userid=models.ForeignKey(user, on_delete=models.CASCADE,null=False)
    advertiserid=models.ForeignKey(advertiser, on_delete=models.CASCADE,null=False)
    biddate=models.DateField(auto_now=True)
    description=models.TextField(max_length=50,null=False)
    status=models.IntegerField(default=0,null=False)

    def __str__(self):
        return str(self. projectbidid)
    
class review(models.Model):
    reviewid=models.AutoField(primary_key=True)
    review=models.TextField(max_length=300)
    rating=models.IntegerField(null=False)
    userid=models.ForeignKey(user, on_delete=models.CASCADE,null=False)
    advertiserid=models.ForeignKey(advertiser, on_delete=models.CASCADE,null=False)
    date=models.TimeField(auto_now=True)
    
    def __str__(self):
        return str(self.reviewid)
    


# class likep(models.Model):
#     likeid=models.IntegerField(primary_key=True)
#     projectid=models.ForeignKey(project,null=False,on_delete=models.CASCADE)
#     date=models.TimeField(auto_now=True)
#     advertiserid=models.ForeignKey(advertiser,null=False, on_delete=models.CASCADE)

#     def __str__(self):
#         return str(self.likeid)

# class tblLike(models.Model):
#     likeId=models.IntegerField(primary_key=True)
#     projectid=models.ForeignKey(project, on_delete=models.CASCADE)
#     date=models.TimeField(auto_now=True)
#     advertiserid=models.ForeignKey(advertiser, on_delete=models.CASCADE)

#     def __str__(self):
#         return str(self.likeId)

class like(models.Model):
    likeId=models.IntegerField(primary_key=True)
    projectid=models.ForeignKey(project, on_delete=models.CASCADE)
    date=models.TimeField(auto_now=True)
    advertiserid=models.ForeignKey(advertiser, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.likeId)

class notification(models.Model):
    notifyid=models.IntegerField(primary_key=True),
    userid=models.IntegerField(null=False)
    userType=models.IntegerField(default=0)
    msg=models.TextField(null=False)
    createdDate=models.DateField(auto_now=True)

    def __str__(self):
        return self.msg

 
class chat(models.Model):
    chatid=models.IntegerField(primary_key=True)
    receiverid=models.IntegerField(null=False)
    senderid=models.IntegerField(null=False)
    message=models.TextField(max_length=500,default=True)
    status=models.IntegerField(default=0)
    createddt=models.DateField(auto_now=True)
    def _str_(self):
         return str(self.chatid) 
         
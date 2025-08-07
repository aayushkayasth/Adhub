from django.urls import path 
from .import views

urlpatterns = [
    # path("base",views.loadBase,name="base"),
    path("",views.dashboard,name="dashboard"),
    path("login",views.login,name="login"),
    path("adminprofile",views.adminprofile,name="adminprofile"),
    path("displayState",views.displayState,name="displayState"),
    path("displayCity",views.displayCity,name="displayCity"),
    path("updCity",views.updCity,name="updCity"),
    path("updState",views.updState,name="updState"),
    path("updcategory",views.updcategory,name="updcategory"),
    path("displayCategory",views.displayCategory,name="displayCategory"),
    path("displaySubcategory",views.displaySubcategory,name="displaySubcategory"),
    path("updSubcategory",views.updsubcategory,name="updSubcategory"),
    path("displayUser",views.displayUser,name="displayUser"),
    path("displayAdvertiser",views.displayAdvertiser,name="displayAdvertiser"),
    path("Projects",views.Projects,name="Projects"),
    path("displayProjectSubcategory",views.displayProjectSubcategory,name="displayProjectSubcategory"),
    path("displayProjectbid",views.displayProjectbid,name="displayProjectbid"),
    path("displayReview",views.displayReview,name="displayReview"),
    path("displayLike",views.displayLike,name="displayLike"),
]
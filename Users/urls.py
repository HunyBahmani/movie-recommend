from django.urls import path , re_path
from django.contrib import admin 
from .views import UserRegisterView , UserLoginView , ProfileView, ChangePasswordView
from Movie import apps
from . import views 

apps_name = 'Users' 

urlpatterns = [
       re_path(r'signup/',UserRegisterView.as_view(),name='signup'), 
       re_path(r'login/',UserLoginView.as_view(),name='login'),
       path("profile/", ProfileView.as_view(), name="profile"),
       path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    ]

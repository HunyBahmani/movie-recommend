from django.urls import path, re_path
from .views import UserRegisterView, UserLoginView, ProfileView, ChangePasswordView, UpdateProfileView

app_name = 'Users'

urlpatterns = [
    re_path(r'signup/', UserRegisterView.as_view(), name='signup'),
    re_path(r'login/', UserLoginView.as_view(), name='login'),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("update-profile/", UpdateProfileView.as_view(), name="update_profile"),  # مسیر جدید
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
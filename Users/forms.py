from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User   
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    username = forms.CharField(widget=forms.TextInput({"class": "signup-box__input", "placeholder": "نام کاربری"}))
    password1 = forms.CharField(widget=forms.PasswordInput({"class": "signup-box__input", "placeholder": "رمز عبور"}))
    password2 = forms.CharField(widget=forms.PasswordInput({"class": "signup-box__input", "placeholder": "تأیید رمز عبور"}))

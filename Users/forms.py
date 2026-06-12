from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
    
    username = forms.CharField(widget=forms.TextInput({
        "class": "signup-box__input", 
        "placeholder": "نام کاربری"
    }))
    
    first_name = forms.CharField(
        required=False,  # اختیاری
        widget=forms.TextInput({
            "class": "signup-box__input", 
            "placeholder": "نام"
        })
    )
    
    last_name = forms.CharField(
        required=False,  # اختیاری
        widget=forms.TextInput({
            "class": "signup-box__input", 
            "placeholder": "نام خانوادگی"
        })
    )
    
    email = forms.EmailField(
        required=False,  # اختیاری
        widget=forms.EmailInput({
            "class": "signup-box__input", 
            "placeholder": "ایمیل (اختیاری)"
        })
    )
    
    password1 = forms.CharField(widget=forms.PasswordInput({
        "class": "signup-box__input", 
        "placeholder": "رمز عبور"
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput({
        "class": "signup-box__input", 
        "placeholder": "تأیید رمز عبور"
    }))



    # اضافه کردن به انتهای فایل forms.py

from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    """فرم ویرایش اطلاعات کاربر"""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'birthdate', 'city', 'gender', 'favgenre')
    
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput({
            "class": "profile__input",
            "placeholder": "نام"
        })
    )
    
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput({
            "class": "profile__input",
            "placeholder": "نام خانوادگی"
        })
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput({
            "class": "profile__input",
            "placeholder": "ایمیل"
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # حذف فیلدهایی که نمی‌خوایم نمایش داده بشن
        self.fields.pop('password')
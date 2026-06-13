from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render 
from django.views.generic import TemplateView , ListView , DetailView
from django.shortcuts import render 
from django.urls import reverse_lazy 
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import CustomUserCreationForm
from Recommendations.models import UserInformationFormovieSuggestions
from django.contrib.auth import login
from django.contrib import messages

class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)

        UserInformationFormovieSuggestions.objects.create(
            user=self.object
        )
        login(self.request, self.object)

        return response
class UserLoginView(LoginView):
    template_name = "login.html"
    def get_success_url(self):
        return reverse_lazy("home") #, kwargs={"pk": self.request.user.pk}

class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "change_password.html"
    success_url = reverse_lazy("profile")
    login_url = "login"
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "رمز عبور با موفقیت تغییر کرد!")
        return response

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile.html"
    context_object_name = "user_profile"
    login_url = "login"
    def get_object(self):
        return self.request.user
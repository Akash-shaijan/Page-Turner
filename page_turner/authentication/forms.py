from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class SignupForm(UserCreationForm):
    
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        
        model = Profile
        
        fields = ("email",)


class LoginForm(AuthenticationForm):

    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
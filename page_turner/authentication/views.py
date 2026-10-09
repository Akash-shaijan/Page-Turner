from django.shortcuts import render, redirect

from django.contrib.auth import login, logout

from django.views import View

from .forms import SignupForm, LoginForm

# Create your views here.

class SignupView(View):
    
    template = "authentication/signup.html"

    def get(self, request, *args, **kwargs):
        
        form = SignupForm()
        
        data= {"form": form}
        
        return render(request, self.template, context=data)

    def post(self, request, *args, **kwargs):
        
        form = SignupForm(data=request.POST)
        
        if form.is_valid():
            
            user = form.save()
            
            login(request, user)
            
            return redirect("home")
        
        
        data = {"form": form}
        
        return render(request, self.template, context=data)


class LoginView(View):
    
    template = "authentication/login.html"

    def get(self, request, *args, **kwargs):
        
        form = LoginForm()
        
        data = {"form": form}
        
        return render(request, self.template, context=data)

    def post(self, request, *args, **kwargs):
        
        
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            
            user = form.get_user()
            
            login(request, user)
            
            next_url = request.POST.get("next") or request.GET.get("next")
            
            return redirect(next_url or "home")

        
        data = {"form": form}
        
        return render(request, self.template, context=data)


class LogoutView(View):
    
    def get(self, request, *args, **kwargs):
        
        logout(request)
        
        return redirect("home")
    
    
    
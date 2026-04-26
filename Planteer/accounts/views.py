from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def sign_up(request: HttpRequest):
    if request.method == "POST":
        try:
            new_user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password"],
                email=request.POST.get("email", ""), 
                first_name=request.POST.get("first_name", ""),
                last_name=request.POST.get("last_name", "")
            )
            
            messages.success(request, "Registered User Successfully", "alert-success")
            return redirect("accounts:sign_in")
            
        except IntegrityError:
            messages.error(request, "Username already exists. Please choose another one.", "alert-danger")
        except Exception as e:
            print(f"Error during registration: {e}")
            messages.error(request, "An error occurred. Please try again.", "alert-danger")

    return render(request, "accounts/signup.html")

def sign_in(request: HttpRequest):
    if request.method == "POST":
        username_val = request.POST.get("username")
        password_val = request.POST.get("password")

        user = authenticate(request, username=username_val, password=password_val)
        
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}", "alert-success")
            return redirect(request.GET.get("next", "main:home_view")) 
        else:
            messages.error(request, "Invalid credentials, please try again.", "alert-danger")

    return render(request, "accounts/signin.html")

def log_out(request: HttpRequest):
    logout(request)
    messages.success(request, "Logged out successfully", "alert-warning")
    
    return redirect("main:home_view")
from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

# Create your views here.

def sign_up_view(request:HttpRequest):

    if request.method=="POST":
        try:
            new_user=User.objects.create_user(
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                username=request.POST["username"],
                email=request.POST["email"],
                password=request.POST["password"]
                )
            new_user.save()
            messages.success(request, "Account created successfully." , "alert-success")
            return redirect("account:sign_in_view")
        except Exception as e:
            print(e)
            messages.error(request, "An error occurred. Please try again." , "alert-danger")
            
    
    return render(request,"account/signup.html")

def sign_in_view(request:HttpRequest):

    if request.method=="POST":
        user=authenticate(
            request,
            username= request.POST["username"],
            password= request.POST["password"]
        )
        if user:
            login(request,user)
            messages.success(request, "Signed in successfully." , "alert-success")
            return redirect("main:home_view")
        else:
            messages.success(request, "Invalid credentials. Please try again." , "alert-danger")

    return render(request,"account/signin.html")

def log_out_view(request:HttpRequest):

    logout(request)
    messages.success(request, "Logged out successfully." , "alert-success")

    return redirect("main:home_view")

@login_required
def profile_view(request):
    return render(request, "account/profile.html")

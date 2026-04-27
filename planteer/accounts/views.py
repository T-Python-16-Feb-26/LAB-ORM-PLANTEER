from django.shortcuts import render
from django.shortcuts import  redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError, transaction

from .models import Profile


# Create your views here.
def sign_up_view(request):
    
    if request.method == 'POST':
        try:
            # ============ making user ============
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            new_user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            new_user.save()
            
            # ============ making profile ============
            profile = Profile(user=new_user,about=request.POST.get('about'), avatar=request.FILES.get('avatar'))
            profile.save()
            
            # ============ end ============
            print(f"new user -> {new_user.username} has signed up")
            #ts myby needs the views.name one but idk
            return redirect('accounts:log_in')
        except IntegrityError as e:
            messages.error(request, "Please choose another username", "alert-danger")

        except Exception as e:
            print(e)
    return render(request, 'accounts/signup.html', {})

def sign_in_view(request):
    if request.method == "POST":

        #checking user credentials
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user:
            #login the user
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Please try again. You credentials are wrong", "alert-danger")


    return render(request, 'accounts/login.html', {})

def log_out(request):
    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")

    return redirect(request.GET.get("next", "/"))

def profile_view(request, user_id):
    
    try:
        user = User.objects.get(username=user_id)
        if not Profile.objects.filter(user=user).first():
            new_profile = Profile(user=user)
            new_profile.save() 
    except Exception as e:
        print(e)
        return redirect(request,'main:home')
    return render(request, 'accounts/profile.html', {"user": user})
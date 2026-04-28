from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import Profile
from django.db import transaction
import os



# Create your views here.


def sign_up(request: HttpRequest):

    if request.method == "POST":

        try:
            print(os.environ.get("EMAIL_HOST_USER"))
            print(os.environ.get("EMAIL_HOST_PASSWORD"))
            new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
            new_user.save()

            profile = Profile.objects.create(user=new_user, about=request.POST["about"], social_link=request.POST["social_link"], avatar=request.FILES.get("avatar", Profile.avatar.field.get_default()))
            profile.save()
            #send confirmation email
            sign_up_html = render_to_string("accounts/mail/confirmation.html", {
                "user_name": new_user.username
            })
            send_to = new_user.email
            email_message = EmailMessage("confiramation", sign_up_html, settings.EMAIL_HOST_USER, [send_to])
            email_message.content_subtype = "html"
            #email_message.connection = email_message.get_connection(True)
            email_message.send()
            messages.success(request, "Registered User Successfuly", "alert-success")
            return redirect("accounts:sign_in")
        except Exception as e:
            messages.error(request, "Couldn't register user. Try again", "alert-danger")
            print(e)
    
    return render(request, "accounts/signup.html", {})


@never_cache
def sign_in(request:HttpRequest):

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
            print("user not found")
            messages.error(request, "Please try again. You credentials are wrong", "alert-danger")



    return render(request, "accounts/signin.html")


def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")

    return redirect(request.GET.get("next", "/"))

def user_profile_view(request:HttpRequest, user_name):

    try:
        user = User.objects.get(username=user_name)
        if not Profile.objects.filter(user=user).first():
            new_profile = Profile(user=user)
            new_profile.save()
        #profile:Profile = user.profile  
        #profile = Profile.objects.get(user=user)
    except Exception as e:
        print(e)
        return render(request,'404.html')
    

    return render(request, 'accounts/profile.html', {"user" : user})

def update_user_profile(request:HttpRequest):

    if not request.user.is_authenticated:
        messages.warning(request, "Only registered users can update their profile", "alert-warning")
        return redirect("accounts:sign_in")
    

    if request.method == "POST":

        try:
            with transaction.atomic():
                user:User = request.user

                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

                profile:Profile = user.profile
                profile.about = request.POST["about"]
                profile.social_link = request.POST["social_link"]
                if "avatar" in request.FILES: profile.avatar = request.FILES["avatar"]
                profile.save()

            messages.success(request, "updated profile successfuly", "alert-success")
        except Exception as e:
            messages.error(request, "Couldn't update profile", "alert-danger")
            print(e)

    return render(request, "accounts/update_profile.html")

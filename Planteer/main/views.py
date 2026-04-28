from django.shortcuts import render, redirect
from plants.models import Plant
from .models import Contact
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def home(request):
    plants = Plant.objects.all()
    return render(request, 'main/home.html', {'plants': plants})


def contact(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # validation
        if first_name and last_name and email and message:
            Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                message=message
            )
            return redirect("contact_messages")

    return render(request, "main/contact.html")


def contact_messages(request):
    messages = Contact.objects.all()
    return render(request, 'main/messages.html', {'messages': messages})

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if username and password:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            return redirect("home")

    return render(request, "main/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "main/login.html")

def logout_view(request):
    logout(request)
    return redirect("home")
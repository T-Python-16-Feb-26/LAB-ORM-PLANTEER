from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from .forms import ContactForm
from .models import Contact
from plants.models import Plant
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("core:home")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect("core:home")

def home_view(request:HttpRequest):
    featured_plants = Plant.objects.all().order_by('-created_at')[:4]
    return render(request, 'core/home.html', {
        'featured_plants': featured_plants
    })

def about_view(request:HttpRequest):
    return render(request, 'core/about.html')

def services_view(request:HttpRequest):
    return render(request, 'core/services.html')


def contact_view(request:HttpRequest):
    success = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            form = ContactForm()
            success = True
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {
        'form': form,
        'success': success,
    })


def contact_messages_view(request:HttpRequest):
    messages = Contact.objects.all().order_by('-created_at')
    return render(request, 'core/contact_messages.html', {
        'messages': messages,
    })

def services_view(request:HttpRequest):
    return render(request, 'core/services.html')
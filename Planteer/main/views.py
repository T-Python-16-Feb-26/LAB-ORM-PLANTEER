from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Contact
from plants.models import Plant

def base_view(request:HttpRequest):
    return render(request, 'main/base.html')

def home_view(request:HttpRequest):
    if request.user.is_authenticated:
        print(request.user.email)
    else:
        print("User is not logged in")
    plants = Plant.objects.all().order_by("-created_at")[0:3]
    return render(request, 'main/home.html', {'plants': plants})

def contact_view(request:HttpRequest):
    if request.method == 'POST':
        Contact.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            message=request.POST.get('message'),
        )
        return redirect('main:contact_view')
    return render(request, 'main/contact.html' )

def mode_view(request:HttpRequest, mode):
    response = redirect(request.GET.get("next", "/"))

    if mode == "light":
        response.set_cookie("mode", "light")
    elif mode == "dark":
        response.set_cookie("mode", "dark")

    return response
def contact_messages_view(request:HttpRequest):
    messages = Contact.objects.all().order_by('-created_at')
    return render(request, 'main/contact_messages.html', {'messages': messages})
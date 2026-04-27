from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from .models import Contact
from plants.models import Plant

# Create your views here.


def home_view(request:HttpRequest):
    plants = Plant.objects.all().order_by("-created_at")[0:3]
    return render(request, "main/home.html" , {"plants": plants})

def contact_view(request:HttpRequest):

    return render(request, "main/contact.html")

def message_view(request:HttpRequest):

    return render(request, "main/message.html")



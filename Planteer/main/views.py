from django.shortcuts import render , redirect
from django.http import HttpRequest,HttpResponse
from plants.models  import Plant
from main.models import Contact
# Create your views here.
def home_view(request:HttpRequest):
    plants=Plant.objects.all()[0:2]

    return render(request,"main/index.html", {"plants":plants})

def Contact_us_view(request:HttpRequest):

    if request.method=="POST":
        new_message=Contact(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            message=request.POST['message'])
        new_message.save()
        return redirect("main:message_view")


    return render(request,"main/Contact-us.html")

def message_view(request:HttpRequest):

    messages=Contact.objects.all()


    return render(request, "main/messages.html", {"messages":messages})

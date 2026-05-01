from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from plant.models import Plant
import random

# Create your views here.
def home_view(request : HttpRequest):
    if request.user.is_authenticated:
        print(request.user.username)
    else:
        print("User is not logged in")
    plants = random.sample(list(Plant.objects.all()), 3)
    return render(request, "main/home_page.html", {"plants": plants})

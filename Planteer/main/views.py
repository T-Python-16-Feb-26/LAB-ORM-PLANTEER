from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from plants.models import Plant 

# Create your views here.

def home_view(request):
    latest_plants = Plant.objects.all().order_by('-created_at')[:3]
    return render(request, "main/home.html", {"plants": latest_plants})
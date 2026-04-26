from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpRequest
from .models import Plant, Review, Country
from django.contrib import messages
from .forms import PlantForm

# Create your views here.

def all_plants_view(request):
    
    all_countries = Country.objects.all()
    
    country_id = request.GET.get('country_filter')

    if country_id:
        plants = Plant.objects.filter(countries__id=country_id)
    else:
        plants = Plant.objects.all()

    return render(request, "plants/all_plants.html", {
        "plants": plants, 
        "all_countries": all_countries  
    })

def plant_detail_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    
    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:4]
    
    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants 
    })

from .models import Plant, Country 

def add_plant_view(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "Access Denied: This page is restricted to staff members only.", "alert-danger")
        return redirect("main:home_view")
    
    countries = Country.objects.all()
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("plants:all_plants_view")
    else:
        form = PlantForm()
    return render(request, "plants/add_plant.html", {"form": form, "countries": countries})

def update_plant_view(request, plant_id):

    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "Access Denied: You do not have permission to edit plant data.", "alert-danger")
        return redirect("plants:plant_detail_view", plant_id=plant_id)
    plant = get_object_or_404(Plant, id=plant_id)
    countries = Country.objects.all() 
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect("plants:plant_detail_view", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)
    return render(request, "plants/update_plant.html", {"form": form, "plant": plant, "countries": countries})


def delete_plant_view(request, plant_id):

    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "Access Denied: You do not have permission to delete plant data.", "alert-danger")
        return redirect("plants:plant_detail_view", plant_id=plant_id)
    
    plant = Plant.objects.get(id=plant_id)
    plant.delete()
    return redirect("plants:all_plants_view")


def search_view(request):
    if "search" in request.GET and len(request.GET["search"]) >= 2:
        results = Plant.objects.filter(name__icontains=request.GET["search"])
    else:
        results = [] 
        
    return render(request, "plants/search.html", {"results": results})


def add_review_view(request: HttpRequest, plant_id):

    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to share your insights.", "alert-warning")
        return redirect("accounts:sign_in")

    plant_object = Plant.objects.get(pk=plant_id)

    if request.method == "POST":
        new_review = Review(
            plant=plant_object, 
            user=request.user, 
            comment=request.POST["comment"]
        )
        new_review.save()

    return redirect("plants:plant_detail_view", plant_id=plant_id)


def country_plants_view(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    plants = Plant.objects.filter(countries=country)
    
    return render(request, 'plants/country_plants.html', {
        'country': country,
        'plants': plants
    })
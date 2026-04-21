from django.shortcuts import render ,redirect
from django.http import HttpRequest,HttpResponse
from .models import Plant, Comment

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import PlantForm
from .models import Plant,Country


def add_plant_view(request: HttpRequest):

    plant_form = PlantForm()

    countries=Country.objects.all()

    if request.method == "POST":
        plant_form = PlantForm(request.POST, request.FILES)

        if plant_form.is_valid():
            plant_form.save()
            return redirect('main:home_view')
        else:
            print("not valid form")

    return render(request, "plants/add_plant.html", {
        "plant_form": plant_form,
        "CategoryChoices": Plant.CategoryChoices.choices,
        "countries":countries,
    })



def plant_detail_view(request: HttpRequest, plant_id):

    plant = Plant.objects.get(pk=plant_id)
    comment=Comment.objects.filter(plant=plant)

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(pk=plant.pk)[:4]

    return render(request, 'plants/plant_detail.html', {"plant": plant, "related_plants": related_plants, "comments":comment})



def plant_update_view(request: HttpRequest, plant_id):

    plant = Plant.objects.get(pk=plant_id)
    countries=Country.objects.all()

    if request.method == "POST":
        plant_form = PlantForm(request.POST, request.FILES, instance=plant)

        if plant_form.is_valid():
            plant_form.save()
            return redirect('plants:plant_detail_view', plant_id=plant.id,)
        else:
            print("not valid form")

    else:
        plant_form = PlantForm(instance=plant)

    return render(request, "plants/plant_update.html", {
        "plant_form": plant_form,
        "CategoryChoices": Plant.CategoryChoices.choices,
        "plant": plant,
        "countries":countries,
    })

def plant_delete_view(request:HttpRequest, plant_id):

     plant=Plant.objects.get(pk=plant_id)
     plant.delete()

     return redirect('main:home_view')


def all_plants_view(request: HttpRequest):
    plants = Plant.objects.all().order_by("name_plant")

    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')
    country= request.GET.get('country')


    if category:
        plants = plants.filter(category=category)

    if is_edible:
        if is_edible == 'true':
            plants = plants.filter(is_edible=True)
        elif is_edible == 'false':
            plants = plants.filter(is_edible=False)
    if country:
        plants = plants.filter(countries__id=country)
    countries = Country.objects.all()


    return render(request, "plants/all_plants.html", {"plants": plants,"categories": Plant.CategoryChoices.choices ,"countries": countries})
    
def search_plants_view(request: HttpRequest):

    if "search" in request.GET:
        plants = Plant.objects.filter(name_plant__contains=request.GET["search"])

        if "order_by" in request.GET and request.GET["order_by"] == "name":
            plants = plants.order_by("name_plant")

        elif "order_by" in request.GET and request.GET["order_by"] == "date":
            plants = plants.order_by("-created_at")

    else:
        plants = []

    return render(request, "plants/search_plant.html", {"plants": plants})


def add_comment_view(request:HttpRequest, plant_id):

    if request.method=="POST":
        plant=Plant.objects.get(pk=plant_id)
        new_comment=Comment(
            plant=plant,
            name= request.POST.get("name"),
            comment= request.POST.get("comment"),
        )
        new_comment.save()

    return redirect("plants:plant_detail_view", plant_id=plant_id)

def country_detail_view(request, country_id):
    country = Country.objects.get(id=country_id)
    plants = Plant.objects.filter(countries=country)

    return render(request, 'plants/country_detail.html', {
        'country': country,
        'plants': plants
    })

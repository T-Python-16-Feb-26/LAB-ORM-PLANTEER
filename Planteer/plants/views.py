from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from .models import Plant , Comment , Country
from .forms import PlantForm

# Create your views here.

def all_view(request: HttpRequest):
    plants = Plant.objects.all()

    if "category" in request.GET and request.GET["category"] != "":
        plants = plants.filter(category=request.GET["category"])

    if "is_edible" in request.GET and request.GET["is_edible"] != "":
        plants = plants.filter(is_edible=request.GET["is_edible"])

    if "country" in request.GET and request.GET["country"] != "":
        plants = plants.filter(countries__id=request.GET["country"])

    return render(request, "plants/all_plants.html", {
        "plants": plants,
        "categories": Plant.Category.choices,
        "countries": Country.objects.all()
        
    })

# def new_view(request: HttpRequest):
#     form = PlantForm()

#     if request.method == "POST":
#         form = PlantForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("plants:all_view")

#     return render(request, "plants/new_plant.html", {
#         "form": form,
#         "countries":Country.objects.all()
#         })
def new_view(request: HttpRequest):
    if not request.user.is_staff:
        return redirect("main:home_view")
    
    form = PlantForm()
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            plant.countries.set(request.POST.getlist("countries"))
            return redirect("plants:all_view")

    return render(request, "plants/new_plant.html", {
        "form": form,
        "countries": Country.objects.all()
    })

def detail_view(request: HttpRequest, plant_id: int):
    plant = Plant.objects.get(pk=plant_id)
    comments=Comment.objects.filter(plant=plant)

    related_plants = Plant.objects.filter(category=plant.category).exclude(pk=plant_id)[:3]
    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "comments": comments,
        "related_plants": related_plants
    })



def update_view(request: HttpRequest, plant_id: int):
    if not request.user.is_staff:
        return redirect("main:home_view")

    plant = Plant.objects.get(pk=plant_id)
    form = PlantForm(instance=plant)

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            plant=form.save()
            plant.countries.set(request.POST.getlist("countries"))
            return redirect("plants:detail_view", plant_id=plant.id)

    return render(request, "plants/update_plant.html", {
        "form": form,
        "plant": plant, 
        "countries":Country.objects.all()
        })



# def delete_view(request: HttpRequest, plant_id: int):
#     return render(request, "plants/plant_detail.html")
def delete_view(request:HttpRequest, plant_id:int):
    if not request.user.is_staff:
        return redirect("main:home_view")

    plant = Plant.objects.get(pk=plant_id)
    plant.delete()
    return redirect("main:home_view")

def search_view(request: HttpRequest):

    # the user have to search with more than 2 letters 3 and on...
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        plants = Plant.objects.filter(name__contains=request.GET["search"])
    
    else:
        plants = []
    return render(request, "plants/search.html", {"plants": plants})

def add_comment_view(request:HttpRequest,plant_id:int):
    if request.method== "POST":
        plant_ob = Plant.objects.get(pk=plant_id)
        new_comment=Comment(plant=plant_ob,user=request.user,content=request.POST['content'])
        new_comment.save()

    return redirect ("plants:detail_view", plant_id=plant_id)
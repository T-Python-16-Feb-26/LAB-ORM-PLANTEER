from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
import os
from .forms import PlantForm
from .models import Category, Plant, Comment, Country
from django.contrib import messages

def add_plant_view(request: HttpRequest):
    if not request.user.is_staff:
        messages.success(request, "only staff can add plants", "alert-warning")
        return redirect('main:home_view')
    if request.method == 'POST':
        name = request.POST.get('name')
        about = request.POST.get('about')
        used_for = request.POST.get('used_for')
        is_edible = request.POST.get('is_edible') == 'on'

        category_ids = request.POST.getlist('categories')
        country_ids = request.POST.getlist('countries')
        image = request.FILES.get('image')

        new_plant = Plant.objects.create(
            name=name,
            about=about,
            used_for=used_for,
            is_edible=is_edible,
            image=image
        )
        new_plant.categories.set(category_ids)
        new_plant.countries.set(country_ids)

        return redirect('plants:all_plants_view', 'all')

    categories = Category.objects.all()
    countries = Country.objects.all()

    return render(request, 'plants/add_plant.html', {
        'categories': categories,
        'countries': countries
    })

def all_plants_view(request: HttpRequest, category_name: str):

    categories = Category.objects.all()
    countries = Country.objects.all()

    selected_categories = request.GET.getlist('category')
    selected_country = request.GET.get('country')
    edible = request.GET.get('edible')

    plants = Plant.objects.all().order_by('-created_at')

    if selected_categories:
        plants = plants.filter(
            categories__name__in=selected_categories
        ).distinct()
    if selected_country:
        plants = plants.filter(
            countries__id=int(selected_country)
        ).distinct()
    if edible == 'true':
        plants = plants.filter(is_edible=True)
    elif edible == 'false':
        plants = plants.filter(is_edible=False)

    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'categories': categories,
        'countries': countries,
        'selected_categories': selected_categories,
        'selected_country': selected_country,
        'edible': edible,
    })

def plant_detail_view(request:HttpRequest, plant_id:int):
    plant = get_object_or_404(Plant, pk=plant_id)
    related = Plant.objects.filter(categories__in=plant.categories.all()).exclude(pk=plant_id)[:3]
    comments = plant.plant_comments.order_by('-created_at')
    if request.method == 'POST' and 'comment_submit' in request.POST:
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(plant=plant, user=request.user, comment=comment_text)
        return redirect('plants:plant_detail_view', plant_id=plant.id)
    return render(request, 'plants/plant_detail.html', {"plant" : plant, "related": related, "comments": comments})

def plant_update_view(request:HttpRequest, plant_id:int):
    plant = Plant.objects.get(pk=plant_id)
    if not request.user.is_staff:
        messages.success(request, "only staff can edit plants", "alert-warning")
        return redirect("plants:plant_detail_view", plant_id=plant.id)
    categories = Category.objects.all()
    countries = Country.objects.all()

    if request.method == "POST":
        plant_form = PlantForm(instance=plant, data=request.POST, files=request.FILES)
        if plant_form.is_valid():
            plant_form.save()
        else:
            print(plant_form.errors)
    
        return redirect("plants:plant_detail_view", plant_id=plant.id)

    return render(request, "plants/update_plant.html", {"plant":plant, "categories" : categories, "countries": countries})


def plant_delete_view(request: HttpRequest, plant_id: int):
    
    plant = Plant.objects.get(pk=plant_id)
    if not request.user.is_staff:
        messages.success(request, "only staff can edit plants", "alert-warning")
        return redirect("plants:plant_detail_view", plant_id=plant.id)
    plant.delete()
    return redirect('plants:all_plants_view', category_name='all')

def search_plants_view(request:HttpRequest):
    categories = Category.objects.all()
    selected_categories = request.GET.getlist('category')
    edible = request.GET.get('edible')

    if "search" in request.GET and len(request.GET["search"]) >= 3:
        plants = Plant.objects.filter(name__contains=request.GET["search"]).order_by("-created_at")
    else:
        plants = Plant.objects.none()

    if selected_categories:
        plants = plants.filter(categories__name__in=selected_categories).distinct()

    if edible == 'true':
        plants = plants.filter(is_edible=True)
    elif edible == 'false':
        plants = plants.filter(is_edible=False)

    return render(request, "plants/search_plants.html", {
        "plants": plants,
        "categories": categories,
        "selected_categories": selected_categories,
        "edible": edible,
    })
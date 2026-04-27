from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.contrib import messages
from .models import Plant, Category, Country, Comment
from .forms import PlantForm, PlantFilterForm, CommentForm


def all_plants(request: HttpRequest):
    plants = Plant.objects.all()
    filter_form = PlantFilterForm(request.GET)

    if filter_form.is_valid():
        name = filter_form.cleaned_data.get('name')
        is_edible = filter_form.cleaned_data.get('is_edible')
        country = filter_form.cleaned_data.get('country')
        if name:
            plants = plants.filter(name__icontains=name)
        if is_edible is not None:
            plants = plants.filter(is_edible=is_edible)
        if country:
            plants = plants.filter(countries=country)

    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'filter_form': filter_form,
        'total': plants.count(),
    })


def plant_detail(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    comments = plant.comments.all()
    comment_form = CommentForm()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.plant = plant
            comment.user = request.user
            comment.save()
            return redirect('plants:plant_detail', plant_id=plant.pk)

    related_plants = plant.get_related_plants()

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants,
        'comments': comments,
        'comment_form': comment_form,
    })


def add_plant(request: HttpRequest):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plant added successfully!')
            return redirect('plants:all_plants')
    else:
        form = PlantForm()

    return render(request, 'plants/plant_form.html', {
        'form': form,
        'action': 'Add',
    })


def update_plant(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plant updated successfully!')
            return redirect('plants:plant_detail', plant_id=plant.pk)
    else:
        form = PlantForm(instance=plant)

    return render(request, 'plants/plant_form.html', {
        'form': form,
        'action': 'Update',
        'plant': plant,
    })


def delete_plant(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == 'POST':
        plant.delete()
        return redirect('plants:all_plants')

    return render(request, 'plants/plant_delete.html', {'plant': plant})


def search_plants(request: HttpRequest):
    plants = Plant.objects.none()
    query = request.GET.get('q', '').strip()
    searched = bool(request.GET)

    if query:
        plants = Plant.objects.filter(name__icontains=query) | Plant.objects.filter(description__icontains=query)

    return render(request, 'plants/search.html', {
        'plants': plants,
        'query': query,
        'searched': searched,
        'result_count': plants.count(),
    })


def plants_by_country(request: HttpRequest, country_id):
    country = get_object_or_404(Country, pk=country_id)
    plants = country.plants.all()

    return render(request, 'plants/plants_by_country.html', {
        'country': country,
        'plants': plants,
        'total': plants.count(),
    })
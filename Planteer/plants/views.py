from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import Plant, Category
from .forms import PlantForm, PlantFilterForm


def all_plants(request: HttpRequest):
    plants = Plant.objects.all()
    filter_form = PlantFilterForm(request.GET)

    if filter_form.is_valid():
        name = filter_form.cleaned_data.get('name')
        is_edible = filter_form.cleaned_data.get('is_edible')
        if name:
            plants = plants.filter(name__icontains=name)
        if is_edible is not None:
            plants = plants.filter(is_edible=is_edible)

    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'filter_form': filter_form,
        'total': plants.count(),
    })


def plant_detail(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    related_plants = plant.get_related_plants()

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants,
    })


def add_plant(request: HttpRequest):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plant added successfully!')
            return redirect('main:home')
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
            plant = form.save()
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
        plants = Plant.objects.filter(name__icontains=query) | \
                 Plant.objects.filter(scientific_name__icontains=query) | \
                 Plant.objects.filter(description__icontains=query)
        plants = plants.distinct()

    return render(request, 'plants/search.html', {
        'plants': plants,
        'query': query,
        'searched': searched,
        'result_count': plants.count(),
    })
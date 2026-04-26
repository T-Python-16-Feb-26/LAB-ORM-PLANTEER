from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Comment, Country
from .forms import PlantForm


def all_plants_view(request):
    plants = Plant.objects.all().order_by('-created_at')

    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')
    country_id = request.GET.get('country')

    if category:
        plants = plants.filter(category=category)

    if is_edible == 'true':
        plants = plants.filter(is_edible=True)
    elif is_edible == 'false':
        plants = plants.filter(is_edible=False)

    if country_id:
        plants = plants.filter(countries__id=country_id)

    return render(request, 'plants/all_plants.html', {
        'plants': plants.distinct(),
        'categories': Plant.Category.choices,
        'countries': Country.objects.all(),
        'selected_category': category,
        'selected_is_edible': is_edible,
        'selected_country': country_id,
    })


def plant_detail_view(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        content = request.POST.get('content', '').strip()

        if name and content:
            Comment.objects.create(
                plant=plant,
                name=name,
                content=content
            )
            return redirect('plants:plant_detail_view', plant_id=plant.id)

    comments = plant.comments.all().order_by('-created_at')
    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:3]

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'comments': comments,
        'related_plants': related_plants,
    })


def add_plant_view(request):
    if request.method == 'POST':
        form = PlantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plants:all_plants_view')
    else:
        form = PlantForm()

    return render(request, 'plants/add_plant.html', {'form': form})


def update_plant_view(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == 'POST':
        form = PlantForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plants:plant_detail_view', plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(request, 'plants/update_plant.html', {'form': form, 'plant': plant})


def delete_plant_view(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == 'POST':
        plant.delete()
        return redirect('plants:all_plants_view')

    return render(request, 'plants/delete_plant.html', {'plant': plant})


def search_view(request):
    query = request.GET.get('search', '').strip()
    plants = Plant.objects.filter(name__icontains=query) if query else []

    return render(request, 'plants/search.html', {
        'plants': plants,
        'query': query,
    })


def country_plants_view(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    plants = country.plants.all()

    return render(request, 'plants/country_plants.html', {
        'country': country,
        'plants': plants,
    })
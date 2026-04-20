# from django.shortcuts import render
# from django.http import HttpRequest

# def home_view(request: HttpRequest):
#     return render(request, 'main/home.html')

# def all_plants_view(request: HttpRequest):
#     return render(request, 'main/all_plants.html')

# def plant_detail_view(request: HttpRequest, plant_id):
#     return render(request, 'main/plant_detail.html', {
#         'plant_id': plant_id
#     })

# def new_plant_view(request: HttpRequest):
#     return render(request, 'main/new_plant.html')

# def update_plant_view(request: HttpRequest, plant_id):
#     return render(request, 'main/update_plant.html')

# def delete_plant_view(request: HttpRequest, plant_id):
#     return render(request, 'main/delete_plant.html')

# def search_plants_view(request: HttpRequest):
#     return render(request, 'main/search_plants.html')
# 1===========
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Plant
# from .forms import PlantForm


# def all_plants_view(request):
#     plants = Plant.objects.all().order_by('-created_at')

#     category = request.GET.get('category')
#     is_edible = request.GET.get('is_edible')

#     if category:
#         plants = plants.filter(category=category)

#     if is_edible == 'true':
#         plants = plants.filter(is_edible=True)
#     elif is_edible == 'false':
#         plants = plants.filter(is_edible=False)

#     context = {
#         'plants': plants,
#         'categories': Plant.CategoryChoices.choices,
#     }
#     return render(request, 'plants/all_plants.html', context)


# def plant_detail_view(request, plant_id):
#     plant = get_object_or_404(Plant, id=plant_id)
#     related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:3]

#     context = {
#         'plant': plant,
#         'related_plants': related_plants,
#     }
#     return render(request, 'plants/plant_detail.html', context)


# def new_plant_view(request):
#     if request.method == 'POST':
#         form = PlantForm(request.POST, request.FILES)
#         if form.is_valid():
#             plant = form.save()
#             return redirect('plants:plant_detail', plant_id=plant.id)
#     else:
#         form = PlantForm()

#     return render(request, 'plants/new_plant.html', {'form': form})


# def update_plant_view(request, plant_id):
#     plant = get_object_or_404(Plant, id=plant_id)

#     if request.method == 'POST':
#         form = PlantForm(request.POST, request.FILES, instance=plant)
#         if form.is_valid():
#             form.save()
#             return redirect('plants:plant_detail', plant_id=plant.id)
#     else:
#         form = PlantForm(instance=plant)

#     return render(request, 'plants/update_plant.html', {'form': form, 'plant': plant})


# def delete_plant_view(request, plant_id):
#     plant = get_object_or_404(Plant, id=plant_id)

#     if request.method == 'POST':
#         plant.delete()
#         return redirect('plants:all_plants')

#     return render(request, 'plants/delete_plant.html', {'plant': plant})


# def search_plants_view(request):
#     query = request.GET.get('q', '')
#     plants = []

#     if query:
#         plants = Plant.objects.filter(name__icontains=query).order_by('-created_at')

#     return render(request, 'plants/search_plants.html', {
#         'plants': plants,
#         'query': query,
#     })

# 2=========
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant
from .forms import PlantForm


def all_plants_view(request):
    plants = Plant.objects.all().order_by('-created_at')

    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')

    if category:
        plants = plants.filter(category=category)

    if is_edible == 'true':
        plants = plants.filter(is_edible=True)
    elif is_edible == 'false':
        plants = plants.filter(is_edible=False)

    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'categories': Plant.Category.choices
    })


def plant_detail_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:3]

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants
    })


def new_plant_view(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        form = PlantForm()

    return render(request, 'plants/new_plant.html', {'form': form})


def update_plant_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(request, 'plants/update_plant.html', {
        'form': form,
        'plant': plant
    })


def delete_plant_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        plant.delete()
        return redirect('plants:all_plants')

    return render(request, 'plants/delete_plant.html', {'plant': plant})


def search_plants_view(request):
    query = request.GET.get('q', '')
    plants = []

    if query:
        plants = Plant.objects.filter(name__icontains=query)

    return render(request, 'plants/search_plants.html', {
        'plants': plants,
        'query': query
    })
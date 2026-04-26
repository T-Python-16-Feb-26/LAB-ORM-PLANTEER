# Imports
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from plants.models import Plant
from main.models import ContactMessage
from .forms import PlantForm


# Create your views here.

# Home page view
def home_view(request):
    plants = Plant.objects.all()[:6]  

    context = {
        'plants': plants,
        'total_count': Plant.objects.count()
    }

    return render(request, 'main/home_page.html', context)

# All plants view with filtering
def all_plants_view(request):
    plants = Plant.objects.all()

    category = request.GET.get('category')
    used_for = request.GET.get('used_for')

    if category:
        plants = plants.filter(category=category)

    if used_for:
        plants = plants.filter(used_for=used_for)

    context = {
        'plants': plants,
        'selected_category': category,
        'selected_used_for': used_for,
    }

    return render(request, 'main/all_plants_page.html', context)

# Plant detail view
def plant_detail_view(request, id):
    plant = Plant.objects.get(id=id)

    return render(request, 'main/plant_detail_page.html', {
        'plant': plant
    })

# Search view
def search_view(request):
    query = request.GET.get('q')

    plants = []

    if query:
        plants = Plant.objects.filter(
            name__icontains=query
        ) | Plant.objects.filter(
            about__icontains=query
        )

    context = {
        'plants': plants,
        'query': query,
    }

    return render(request, 'main/search_page.html', context)

# Contact view
def contact_view(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            message=message
        )

        return redirect('main:messages')

    return render(request, 'main/contact_page.html')

# Messages view
def messages_view(request):
    messages = ContactMessage.objects.all().order_by('-created_at')

    return render(request, 'main/messages_page.html', {
        'messages': messages
    })
    

# CREATE
def add_plant_view(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:all_plants')
    else:
        form = PlantForm()

    return render(request, 'main/add_plant.html', {'form': form})


# UPDATE
def update_plant_view(request, id):
    plant = get_object_or_404(Plant, id=id)

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('main:plant_detail', id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(request, 'main/update_plant.html', {'form': form, 'plant': plant})


# DELETE
def delete_plant_view(request, id):
    plant = get_object_or_404(Plant, id=id)

    if request.method == "POST":
        plant.delete()
        return redirect('main:all_plants')

    return render(request, 'main/delete_plant.html', {'plant': plant})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Comment, Country, Publisher
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def add_plant(request):
    if not request.user.is_superuser:
        return redirect("home")

    countries = Country.objects.all()
    publishers = Publisher.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

     
        if not name or len(name) < 2:
            return render(request, 'plants/add.html', {
                'error': 'Name must be at least 2 characters',
                'countries': countries,
                'publishers': publishers
            })

        if not description or len(description) < 5:
            return render(request, 'plants/add.html', {
                'error': 'Description must be at least 5 characters',
                'countries': countries,
                'publishers': publishers
            })

        publisher_id = request.POST.get("publisher")
        publisher_obj = get_object_or_404(Publisher, id=publisher_id)

        plant = Plant.objects.create(
            name=name,
            description=description,
            image=request.FILES.get('image'),
            category=request.POST.get('category'),
            is_edible=True if request.POST.get('is_edible') else False,
            publisher=publisher_obj
        )

        countries_selected = request.POST.getlist('countries')
        plant.countries.set(countries_selected)

        return redirect('all_plants')

    return render(request, 'plants/add.html', {
        'countries': countries,
        'publishers': publishers
    })


def all_plants(request):
    plants_list = Plant.objects.all().order_by('-id')
    countries = Country.objects.all()

    country_id = request.GET.get('country')
    category = request.GET.get('category')
    is_edible = request.GET.get('edible')

    if country_id:
        plants_list = plants_list.filter(countries__id=country_id)

    if category:
        plants_list = plants_list.filter(category=category)

    if is_edible == "yes":
        plants_list = plants_list.filter(is_edible=True)
    elif is_edible == "no":
        plants_list = plants_list.filter(is_edible=False)

    paginator = Paginator(plants_list, 6)
    page_number = request.GET.get('page')
    plants = paginator.get_page(page_number)

    return render(request, 'plants/all.html', {
        'plants': plants,
        'countries': countries
    })


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    comments = plant.comments.all().order_by('-created_at')
    related = Plant.objects.filter(category=plant.category).exclude(id=plant.id)

    return render(request, 'plants/detail.html', {
        'plant': plant,
        'related': related,
        'comments': comments
    })



def update_plant(request, plant_id):
    if not request.user.is_superuser:
        return redirect("home")

    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        plant.name = request.POST.get('name')
        plant.description = request.POST.get('description')
        plant.category = request.POST.get('category')
        plant.is_edible = True if request.POST.get('is_edible') else False

        if request.FILES.get('image'):
            plant.image = request.FILES.get('image')

        plant.save()
        return redirect('plant_detail', plant_id=plant.id)

    return render(request, 'plants/update.html', {'plant': plant})



def delete_plant(request, plant_id):
    if not request.user.is_superuser:
        return redirect("home")

    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        plant.delete()
        return redirect('all_plants')

    return render(request, 'plants/delete.html', {'plant': plant})



def search_plants(request):
    plants = Plant.objects.all()
    countries = Country.objects.all()
    publishers = Publisher.objects.all()

    query = request.GET.get('q')

    if query:
        plants = (
            plants.filter(name__icontains=query) |
            plants.filter(description__icontains=query) |
            plants.filter(category__icontains=query)
        )

    category = request.GET.get('category')
    if category:
        plants = plants.filter(category=category)

    is_edible = request.GET.get('edible')
    if is_edible == "yes":
        plants = plants.filter(is_edible=True)
    elif is_edible == "no":
        plants = plants.filter(is_edible=False)

    country_id = request.GET.get('country')
    if country_id:
        plants = plants.filter(countries__id=country_id)

    publisher_id = request.GET.get('publisher')
    if publisher_id:
        plants = plants.filter(publisher__id=publisher_id)

    return render(request, 'plants/search.html', {
        'plants': plants,
        'countries': countries,
        'publishers': publishers
    })

@login_required
def add_comment(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        text = request.POST.get('comment')

        if text and len(text) >= 3:
            Comment.objects.create(
                plant=plant,
                user=request.user,
                text=text
            )

    return redirect('plant_detail', plant_id=plant.id)



def plants_by_country(request, country_id):
    plants = Plant.objects.filter(countries__id=country_id)
    return render(request, 'plants/all.html', {'plants': plants})


def publishers_list(request):
    publishers = Publisher.objects.all()
    return render(request, 'plants/publishers.html', {
        'publishers': publishers
    })


def plants_by_publisher(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    plants = publisher.plants.all()

    return render(request, 'plants/publisher_detail.html', {
        'publisher': publisher,
        'plants': plants
    })
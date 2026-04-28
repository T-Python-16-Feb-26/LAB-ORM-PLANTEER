from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Comment, Country
from .forms import PlantForm


def all_plants_view(request):
    plants = Plant.objects.all()

    category = request.GET.get('category')
    edible = request.GET.get('edible')
    country = request.GET.get('country')

    if category:
        plants = plants.filter(category=category)

    if edible == 'true':
        plants = plants.filter(is_edible=True)

    if country:
        plants = plants.filter(countries__id=country)

    countries = Country.objects.all()

    return render(request, 'plants/all.html', {
        'plants': plants,
        'categories': Plant.Category.choices,
        'selected_category': category,
        'selected_edible': edible,
        'selected_country': country,
        'countries': countries,
    })


def plant_detail_view(request, id):
    plant = get_object_or_404(Plant, id=id)
    comments = plant.comments.all().order_by('-created_at')
    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:3]

    if request.method == 'POST':
        if request.user.is_authenticated:
            Comment.objects.create(
                plant=plant,
                user=request.user,
                name=request.user.username,
                content=request.POST.get('content'),
            )
        return redirect(f'/plants/{id}/detail/')

    return render(request, 'plants/detail.html', {
        'plant': plant,
        'comments': comments,
        'related_plants': related_plants,
    })


def create_plant_view(request):
    if not request.user.is_staff:
        return redirect('/')

    if request.method == 'POST':
        name = request.POST.get('name')
        about = request.POST.get('about')
        used_for = request.POST.get('used_for')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        is_edible = request.POST.get('is_edible') == 'on'

        Plant.objects.create(
            name=name,
            about=about,
            used_for=used_for,
            image=image,
            category=category,
            is_edible=is_edible
        )

        return redirect('/plants/all/')

    return render(request, 'plants/new.html')


def update_plant_view(request, id):
    if not request.user.is_staff:
        return redirect('/')

    plant = get_object_or_404(Plant, id=id)

    if request.method == 'POST':
        plant.name = request.POST.get('name')
        plant.about = request.POST.get('about')
        plant.used_for = request.POST.get('used_for')

        image = request.FILES.get('image')
        if image:
            plant.image = image

        category = request.POST.get('category')
        if not category:
            category = plant.category

        plant.category = category
        plant.is_edible = request.POST.get('is_edible') == 'on'
        plant.save()
        return redirect('/plants/all/')

    return render(request, 'plants/update.html', {'plant': plant})


def delete_plant_view(request, id):
    if not request.user.is_staff:
        return redirect('/')

    plant = get_object_or_404(Plant, id=id)
    plant.delete()
    return redirect('/plants/all/')


def search_view(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    edible = request.GET.get('edible')

    plants = Plant.objects.all()

    category_match = None
    for value, label in Plant.Category.choices:
        if query.lower() == label.lower():
            category_match = value
            break

    if category_match:
        plants = plants.filter(category=category_match)
        category = category_match
    elif query:
        plants = plants.filter(name__icontains=query)

    if category and not category_match:
        plants = plants.filter(category=category)

    if edible == 'true':
        plants = plants.filter(is_edible=True)

    return render(request, 'plants/all.html', {
        'plants': plants,
        'categories': Plant.Category.choices,
        'selected_category': category,
        'selected_edible': edible
    })


def add_plant(request):
    if not request.user.is_staff:
        return redirect('/')

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_plants')
    else:
        form = PlantForm()

    return render(request, 'plants/new.html', {'form': form})


def country_plants_view(request, id):
    country = get_object_or_404(Country, id=id)
    plants = Plant.objects.filter(countries__id=id)

    return render(request, 'plants/country_plants.html', {
        'country': country,
        'plants': plants,
    })


def toggle_favourite(request, id):
    get_object_or_404(Plant, id=id)
    redirect_url = request.GET.get('next', '/plants/all/')
    response = redirect(redirect_url)

    favs = request.COOKIES.get('favs', '')
    fav_list = [f for f in favs.split(',') if f]

    if str(id) in fav_list:
        fav_list.remove(str(id))
    else:
        fav_list.append(str(id))

    response.set_cookie('favs', ','.join(fav_list), max_age=60*60*24*30)
    return response
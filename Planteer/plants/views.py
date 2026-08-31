from django.http import HttpRequest
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from better_profanity import profanity
from django.contrib import messages

from .models import Plant, Comment, Country

profanity.load_censor_words()

def all_plant_view(request: HttpRequest):
    plants = Plant.objects.all().order_by('-created_at')
    countries = Country.objects.all().order_by('name')

    selected_category = request.GET.get('category', '').strip()
    selected_country = request.GET.get('country', '').strip()
    selected_is_edible = request.GET.get('is_edible', '').strip().lower()

    valid_categories = [choice[0] for choice in Plant.CategoryChoices.choices]
    if selected_category in valid_categories:
        plants = plants.filter(category=selected_category)

    valid_country_ids = {str(country.id) for country in countries}
    if selected_country in valid_country_ids:
        plants = plants.filter(countries__id=selected_country)

    if selected_is_edible == 'true':
        plants = plants.filter(is_edible=True)
    elif selected_is_edible == 'false':
        plants = plants.filter(is_edible=False)

    plants = plants.distinct()

    context = {
        'plants': plants,
        'categories': Plant.CategoryChoices.choices,
        'countries': countries,
        'selected_category': selected_category,
        'selected_country': selected_country,
        'selected_is_edible': selected_is_edible,
    }
    return render(request, 'plants/all_plants.html', context)

def plant_detail_view(request: HttpRequest, plant_id: int):

    plant = get_object_or_404(Plant, id=plant_id)

    comments = Comment.objects.filter(plant=plant)

    related_plants = (
        Plant.objects
        .filter(category=plant.category)
        .exclude(id=plant.id)
        .order_by('-created_at')[:3]
    )

    context = {
        'plant': plant,
        'comments': comments,
        'related_plants': related_plants,
    }
    return render(request, 'plants/plant_detail.html', context)

def add_plant_view(request: HttpRequest):

    countries = Country.objects.all()

    if not (request.user.is_staff and request.user.has_perm("plants.add_plant")):
        messages.warning(request, "You do not have permission to add a plant.", extra_tags='alert-warning')
        return redirect("main:home_view")

    if request.method == 'POST':
        is_edible = request.POST.get('is_edible', '').strip().lower() == 'true'
        new_plant = Plant(name = request.POST.get('name'),
                          category = request.POST.get('category'),
                          about = request.POST.get('about'),
                          is_edible = is_edible,
                          used_for = request.POST.get('used_for'),
                          image = request.FILES.get('image'),
                        )
        new_plant.save()
        new_plant.countries.set(request.POST.getlist('countries'))
        return redirect("main:home_view")

    return render(request, 'plants/add_plant.html', {'countries': countries})

def update_plant_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, id=plant_id)
    countries = Country.objects.all()

    if not (request.user.is_staff and request.user.has_perm("plants.change_plant")):
        messages.warning(request, "You do not have permission to update this plant.", extra_tags='alert-warning')
        return redirect("main:home_view")

    if request.method == 'POST':
        plant.name = request.POST.get('name', '').strip()
        plant.about = request.POST.get('about', '').strip()
        plant.used_for = request.POST.get('used_for', '').strip()
        plant.is_edible = request.POST.get('is_edible', '').strip().lower() == 'true'

        category = request.POST.get('category', '').strip()
        valid_categories = [choice[0] for choice in Plant.CategoryChoices.choices]
        if category in valid_categories:
            plant.category = category

        image = request.FILES.get('image')
        if image:
            plant.image = image

        plant.save()
        plant.countries.set(request.POST.getlist('countries'))
        return redirect('plants:plant_detail_view', plant_id=plant.id)

    context = {
        'plant': plant,
        'categories': Plant.CategoryChoices.choices,
        'countries': countries,
    }
    return render(request, 'plants/update_plant.html', context)

def delete_plant_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, id=plant_id)

    if not (request.user.is_staff and request.user.has_perm("plants.delete_plant")):
        messages.warning(request, "You do not have permission to delete this plant.", extra_tags='alert-warning')
        return redirect("main:home_view")

    if request.method == 'POST':
        plant.delete()
        return redirect('plants:all_plant_view')

    return redirect('plants:plant_detail_view', plant_id=plant.id)

def search_plant_view(request: HttpRequest):

    countries = Country.objects.all().order_by('name')

    search_query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()
    selected_country = request.GET.get('country', '').strip()
    selected_is_edible = request.GET.get('is_edible', '').strip().lower()

    plants = Plant.objects.all().order_by('-created_at')

    if search_query:
        plants = plants.filter(
            Q(name__icontains=search_query)
            | Q(about__icontains=search_query)
            | Q(used_for__icontains=search_query)
        )

    valid_categories = [choice[0] for choice in Plant.CategoryChoices.choices]
    if selected_category in valid_categories:
        plants = plants.filter(category=selected_category)

    valid_country_ids = {str(country.id) for country in countries}
    if selected_country in valid_country_ids:
        plants = plants.filter(countries__id=selected_country)

    if selected_is_edible == 'true':
        plants = plants.filter(is_edible=True)
    elif selected_is_edible == 'false':
        plants = plants.filter(is_edible=False)

    context = {
        'plants': plants,
        'categories': Plant.CategoryChoices.choices,
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_is_edible': selected_is_edible,
        'selected_country': selected_country,
        'countries': countries,
    }
    return render(request, 'plants/search_plant.html', context)

def add_comment_view(request: HttpRequest, plant_id: int):

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add a comment.", extra_tags='alert-danger')
        return redirect("accounts:sign_in")
    
    if request.method == "POST":
        plant_object = Plant.objects.get(pk=plant_id)
        user = request.user
        text = profanity.censor(request.POST.get("text", "").strip())
        new_comment = Comment(plant=plant_object, user=user, text=text)
        new_comment.save()

        messages.success(request, "Your comment has been added successfully!", extra_tags='alert-success')

    return redirect("plants:plant_detail_view", plant_id=plant_id)

def delete_comment_view(request: HttpRequest, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to delete a comment.", extra_tags='alert-danger')
        return redirect('accounts:sign_in')

    if not (request.user == comment.user or request.user.has_perm("plants.delete_comment")):
        messages.warning(request, "You do not have permission to delete this comment.", extra_tags='alert-warning')
        return redirect('plants:plant_detail_view', plant_id=comment.plant.id)

    if request.method == 'POST':
        plant_id = comment.plant.id
        comment.delete()
        messages.success(request, "Comment deleted successfully.", extra_tags='alert-success')
        return redirect('plants:plant_detail_view', plant_id=plant_id)

    return redirect('plants:plant_detail_view', plant_id=comment.plant.id)

def plants_by_country_view(request: HttpRequest, country_id: int):
    country = get_object_or_404(Country, id=country_id)
    plants = Plant.objects.filter(countries__id=country_id).order_by('-created_at')

    context = {
        'country': country,
        'plants': plants,
    }
    return render(request, 'plants/plants_by_country.html', context)
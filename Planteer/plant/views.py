from django.shortcuts import get_object_or_404, render , redirect
from django.http import HttpRequest, HttpResponse
from .models import Plant , Comment , Country
from .forms import PlantForm
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
def plants_view(request : HttpRequest):
    plants = Plant.objects.all()
    countries = Country.objects.all()
    search = request.GET.get('search')
    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')
    country = request.GET.get('country')

    if search:
        plants = plants.filter(name__icontains=search)
    if category:
        plants = plants.filter(category=category)
    if country:
        plants = plants.filter(countries=country)
    if is_edible == "true":
        plants = plants.filter(is_edible=True)
    elif is_edible == "false":
        plants = plants.filter(is_edible=False)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(plants, 6)
    plants_page= paginator.get_page(page_number)

    return render(request, "plant/show_plant.html", {"plants": plants_page, "countries": countries})

def new_plant_view(request : HttpRequest):

    if not (request.user.is_staff and request.user.has_perm("plant.add_plant")):
        messages.warning(request, "You do not have permission to add a plant.", "alert-warning")
        return redirect('main:home_view')

    countries = Country.objects.all()
    if request.method == "POST":
        plant_form = PlantForm(request.POST, request.FILES)
        if plant_form.is_valid():
            plant_form.save()
            messages.success(request, "Plant created successfully.","alert-success")
            return redirect('plant:plants_view')
    else:
        plant_form = PlantForm()
        return render(request, 'plant/new_plant_page.html', {'form': plant_form, 'countries': countries})

        
    return render(request, "plant/new_plant_page.html")

def detail_plant_view(request : HttpRequest, plant_id):

    plant = get_object_or_404(Plant, pk=plant_id)
    related_plants = Plant.objects.filter(category=plant.category).exclude(pk=plant_id)
    comments = Comment.objects.filter(plant=plant)

    return render(request, "plant/detail_plant_page.html", {"plant": plant,"related_plants": related_plants, "comments": comments})

def update_plant_view(request : HttpRequest, plant_id):
    if not request.user.is_staff:
        messages.error(request, "You must be a staff member to update a plant.", "alert-danger")
        return redirect('main:home_view')

    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == "POST":
        plant_form = PlantForm(request.POST, request.FILES, instance=plant)
        if plant_form.is_valid():
            plant_form.save()
            return redirect('plant:plants_view')
    else:
        plant_form = PlantForm(instance=plant)
    
    return render(request, "plant/update_plant_page.html", {"plant": plant , "form": plant_form})

def delete_plant_view(request : HttpRequest, plant_id):
    if not request.user.is_staff:
        messages.error(request, "You must be a staff member to delete a plant.", "alert-danger")
        return redirect('main:home_view')

    try:
        plant = get_object_or_404(Plant, pk=plant_id)
        if request.method == "POST":
            plant.delete()
            messages.success(request, "Plant deleted successfully.","alert-success")
            return redirect('plant:plants_view')
    except Exception as e:
        print(f"Error deleting plant: {e}")
        messages.error(request, "Error occurred while deleting the plant.", "alert-danger")
    return render(request, "plant/delete_plant_page.html", {"plant": plant})
def search_plant_view(request : HttpRequest):
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        plant = Plant.objects.filter(name__contains=request.GET["search"])
    else:
        plant = []
    
    return render(request, "plant/search_plant_page.html",{"plant": plant})

def add_comment_view(request : HttpRequest, plant_id):

    
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add a comment.", "alert-danger")
        return redirect('accounts:signin_view')

    if request.method == "POST":
        plant_object = Plant.objects.get(pk=plant_id)
        new_comment = Comment(plant=plant_object,user=request.user,comment=request.POST["comment"])
        new_comment.save()

        messages.success(request, "Comment added successfully.","alert-success")

    return redirect('plant:detail_plant_view', plant_id=plant_id)


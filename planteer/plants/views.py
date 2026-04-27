from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Comments, Country
from .forms import PlantForm
from django.contrib import messages


app_name = "plants"

#TODO: make the details view be here
# Create your views here.
def all_plants_view(request):
    plants = Plant.objects.all()
    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')
    country = request.GET.get('country')
    
    
    if category:
        plants = plants.filter(category=category)
    if is_edible in ('true', 'false'):
        plants = plants.filter(is_edible=(is_edible == 'true'))
    if country:
        plants = plants.filter(countries__id=country)
        
    return render(request, 'plants/plants-all.html', {
        'plants': plants,
        'categories': Plant.Category.choices,
        'selected_category': category,
        'selected_edible': is_edible,
        'countries': Country.objects.all(),
        'selected_country': country,
        
    })

def plant_detail_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    Co = Country.objects.all()
    comments = Comments.objects.filter(plant=plant)

    related = Plant.objects.filter(category=plant.category).exclude(id=plant.id)
    return render(request, 'plants/plant-detail.html', {'plant': plant, 'related': related, 'comments': comments, 'counties':Co})

#============= searching =============
def search_view(request):
    query = request.GET.get('q')
    plants = Plant.objects.filter(name__icontains=query) if query else Plant.objects.none()
    return render(request, 'plants/search.html', {'plants': plants, 'query': query})


# ============= crud stuff =============
def create_view(request):
    if not request.user.is_staff:
        messages.warning(request, "only staff can add plants", "alert-warning")
        return redirect("main:home")
    form = PlantForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('plants:all_plants_view')
    return render(request, 'plants/create.html', {'form': form})

def update_view(request, plant_id):
    if not request.user.is_staff:
        messages.warning(request, "only staff can add plants", "alert-warning")
        return redirect("main:home")
    plant = get_object_or_404(Plant, id=plant_id)
    form = PlantForm(request.POST or None, request.FILES or None, instance=plant)
    if form.is_valid():
        form.save()
        return redirect('plants:plant_detail_view', plant_id=plant.id)
    return render(request, 'plants/edit.html', {'form': form, 'plant': plant})

def delete_view(request, plant_id):
    if not request.user.is_staff:
        messages.warning(request, "only staff can add plants", "alert-warning")
        return redirect("main:home")
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        plant.delete()
        return redirect('plants:all_plants_view')
    return redirect('plants:plant_detail_view', plant_id=plant_id)

# ============= comment crud stuff =============

def comment_create_view(request, plant_id):
    if not request.user.is_authenticated:
        messages.error(request, "Only registered user can add comments","alert-danger")
        return redirect("accounts:sign_in")
    
    if request.method == 'POST':
        plant = get_object_or_404(Plant, id=plant_id)
        new_comment = Comments(plant=plant, user=request.user, name=request.POST.get('name'),comment=request.POST.get('comment'))
        new_comment.save()
    return redirect('plants:plant_detail_view', plant_id=plant_id)


    

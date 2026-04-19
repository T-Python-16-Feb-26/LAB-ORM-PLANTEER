from django.shortcuts import render ,redirect
from django.http import HttpRequest,HttpResponse
from .models import Plant

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import PlantForm
from .models import Plant


def add_plant_view(request: HttpRequest):

    plant_form = PlantForm()

    if request.method == "POST":
        plant_form = PlantForm(request.POST, request.FILES)

        if plant_form.is_valid():
            plant_form.save()
            return redirect('main:home_view')
        else:
            print("not valid form")

    return render(request, "plants/add_plant.html", {
        "plant_form": plant_form,
        "CategoryChoices": Plant.CategoryChoices.choices
    })
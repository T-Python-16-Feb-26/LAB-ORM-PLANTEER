from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Plant, Comment, Country
from django.core.paginator import Paginator
from .forms import PlantForm
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required



def plants_page(request: HttpRequest):
    plants = Plant.objects.all().prefetch_related("countries")

    search_query = request.GET.get("search", "")
    selected_category = request.GET.get("category", "")
    selected_country = request.GET.get("country", "")
    selected_is_edible = request.GET.get("is_edible", "")
    if search_query:
        plants = plants.filter(name__icontains=search_query)

    if selected_category:
        plants = plants.filter(category=selected_category)

    if selected_country:
        plants = plants.filter(countries__id=selected_country)

    if selected_is_edible == "true":
        plants = plants.filter(is_edible=True)
    elif selected_is_edible == "false":
        plants = plants.filter(is_edible=False)

    plants = plants.distinct()
    plants_preview = plants[:6]

    return render(request, "plants/plants_page.html", {
        "plants": plants_preview, 
        "total_count": plants.count(),
        "categories": Plant.CategoryChoices.choices,
        "countries": Country.objects.all(),
        "search_query": search_query,
        "selected_category": selected_category,
        "selected_country": selected_country,
        "selected_is_edible": selected_is_edible,
    })



def view_plants(request: HttpRequest):
    plants = Plant.objects.all().prefetch_related("countries")
    countries = Country.objects.all()

    selected_category = request.GET.get("category", "")
    selected_is_edible = request.GET.get("is_edible", "")
    selected_country = request.GET.get("country", "")
    search_query = request.GET.get("search", "")

    if selected_category:
        plants = plants.filter(category=selected_category)

    if selected_is_edible == "true":
        plants = plants.filter(is_edible=True)
    elif selected_is_edible == "false":
        plants = plants.filter(is_edible=False)

    if selected_country:
        plants = plants.filter(countries__id=selected_country)

    if search_query:
        plants = plants.filter(name__icontains=search_query)

    plants = plants.distinct()

    paginator = Paginator(plants, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "plants/view_plants.html", {
        "plants": page_obj,
        "page_obj": page_obj,
        "categories": Plant.CategoryChoices.choices,
        "countries": countries,
        "selected_category": selected_category,
        "selected_is_edible": selected_is_edible,
        "selected_country": selected_country,
        "search_query": search_query,
    })


def plant_detail(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        if request.user.is_authenticated:
            content = request.POST.get("content")

            if content:
                Comment.objects.create(
                    plant=plant,
                    user=request.user,
                    content=content
                )

        return redirect('plants:plant_detail', plant_id=plant.id)

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:4]

    comments = plant.comments.order_by('-created_at')

    context = {
        'plant': plant,
        'related_plants': related_plants,
        'comments': comments,
    }

    return render(request, 'plants/plant_detail.html', context)


def country_plants(request: HttpRequest, country_id: int):
    country = get_object_or_404(Country, id=country_id)

    plants = Plant.objects.filter(
        countries=country
    ).prefetch_related("countries")

    return render(request, "plants/country_plants.html", {
        "country": country,
        "plants": plants,
    })

@staff_member_required
def plant_create(request:HttpRequest):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('plants:plants_page')
    else:
        form = PlantForm()

    return render(request, 'plants/plant_form.html', {
        'form': form,
        'page_title': 'Add New Plant'
    })

@staff_member_required
def plant_update(request, plant_id:HttpRequest):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(request, 'plants/plant_form.html', {
        'form': form,
        'page_title': 'Update Plant'
    })

@staff_member_required
def plant_delete(request, plant_id:HttpRequest):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        plant.delete()
        return redirect('plants:plants_page')

    return render(request, 'plants/plant_confirm_delete.html', {
        'plant': plant
    })

def search_plants(request:HttpRequest):
    search_query = request.GET.get('search', '').strip()
    category = request.GET.get('category', '')
    is_edible = request.GET.get('is_edible', '')

    plants = Plant.objects.all()

    if search_query:
        plants = plants.filter(name__icontains=search_query)

    if category:
        plants = plants.filter(category=category)

    if is_edible:
        plants = plants.filter(is_edible=True)

    context = {
        'plants': plants,
        'search_query': search_query,
        'selected_category': category,
        'selected_edible': is_edible,
    }

    return render(request, 'plants/plants_page.html', context)


def bilingual_plant_reply(plant):
    return (
        f"أقترح عليك: {plant.name}\n"
        f"نبذة: {plant.about}\n"
        f"الإضاءة: {plant.light_requirement}\n"
        f"الري: {plant.watering}\n\n"
        f"Suggested plant: {plant.name}\n"
        f"About: {plant.about}\n"
        f"Light: {plant.light_requirement}\n"
        f"Watering: {plant.watering}\n\n"
        f"هل تريد اقتراح اخر؟ اذا قم بكتابة خيار اخر\n"
        f"If you want another option, type: another option"
    )


def bilingual_no_result():
    return (
        "ما لقيت نبات مناسب، جرّب تكتب مواصفات مختلفة.\n\n"
        "I couldn't find a suitable plant. Try different preferences."
    )


def bilingual_no_more_options():
    return (
        "ما عندي خيارات إضافية، جرّب تغيّر طلبك.\n\n"
        "I don't have more options. Try changing your request."
    )


def find_plant(request):
    chat_history = request.session.get("plant_chat_history", [])
    suggestion_ids = request.session.get("plant_suggestion_ids", [])
    current_index = request.session.get("plant_current_index", 0)

    if request.method == "POST":
        original_message = request.POST.get("message", "").strip()
        user_message = original_message.lower()

        if original_message:
            chat_history.append({
                "sender": "user",
                "text": original_message
            })

            if (
                "خيار ثاني" in user_message
                or "خيار آخر" in user_message
                or "another option" in user_message
                or "second option" in user_message
            ):
                if suggestion_ids and current_index + 1 < len(suggestion_ids):
                    current_index += 1
                    plant = Plant.objects.get(id=suggestion_ids[current_index])
                    reply = bilingual_plant_reply(plant)
                else:
                    reply = bilingual_no_more_options()

            else:
                plants = Plant.objects.all()

                if "داخلية" in user_message or "indoor" in user_message:
                    plants = plants.filter(category="indoor")

                if "خارجية" in user_message or "outdoor" in user_message:
                    plants = plants.filter(category="outdoor")

                if (
                    "صالحة للأكل" in user_message
                    or "للأكل" in user_message
                    or "edible" in user_message
                ):
                    plants = plants.filter(is_edible=True)

                if (
                    "قليلة الري" in user_message
                    or "ما تحتاج ري" in user_message
                    or "rarely" in user_message
                    or "low watering" in user_message
                ):
                    plants = plants.filter(watering__icontains="Rare")

                if (
                    "إضاءة منخفضة" in user_message
                    or "غرفة مظلمة" in user_message
                    or "low light" in user_message
                    or "dark room" in user_message
                ):
                    plants = plants.filter(light_requirement__icontains="Low")

                plants = list(plants)

                if plants:
                    suggestion_ids = [plant.id for plant in plants]
                    current_index = 0
                    plant = plants[0]
                    reply = bilingual_plant_reply(plant)
                else:
                    suggestion_ids = []
                    current_index = 0
                    reply = bilingual_no_result()

            chat_history.append({
                "sender": "bot",
                "text": reply
            })

            request.session["plant_chat_history"] = chat_history
            request.session["plant_suggestion_ids"] = suggestion_ids
            request.session["plant_current_index"] = current_index

    return render(request, "plants/find_plant.html", {
        "chat_history": chat_history
    })
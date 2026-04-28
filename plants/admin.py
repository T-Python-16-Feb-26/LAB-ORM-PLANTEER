from django.contrib import admin
from .models import Plant, Comment, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_edible", "created_at")
    list_filter = ("category", "is_edible", "countries")
    search_fields = ("name", "about", "used_for")

    fields = (
        "name",
        "image",
        "category",
        "about",
        "used_for",
        "light_requirement",
        "watering",
        "is_edible",
        "countries",
    )

    filter_horizontal = ("countries",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "plant", "created_at")
    search_fields = ("user__username", "content")
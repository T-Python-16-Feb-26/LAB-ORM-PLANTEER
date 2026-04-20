from django.contrib import admin
from .models import Category, Plant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_edible', 'created_at']
    list_filter = ['category', 'is_edible']
    search_fields = ['name', 'scientific_name']
from django.contrib import admin
from .models import Category, Plant, Country, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_edible', 'created_at']
    list_filter = ['category', 'is_edible']
    search_fields = ['name', 'scientific_name']
    filter_horizontal = ['countries']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'plant', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'body']
from django.contrib import admin
from .models import Plant, Category, Country, Comment
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_edible', 'created_at')
    list_filter = ('is_edible', 'categories', 'countries')
    search_fields = ('name', 'about', 'used_for')
admin.site.register(Plant, PlantAdmin)
admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Comment)

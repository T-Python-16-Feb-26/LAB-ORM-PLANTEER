from django.contrib import admin
from .models import Plant, Review, Country

class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_edible', 'created_at')
    
    search_fields = ('name', 'about', 'used_for')
    
    list_filter = ('category', 'is_edible', 'created_at')
    
    ordering = ('-created_at',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'plant', 'created_at')
    
    search_fields = ('name', 'comment')
    
    list_filter = ('plant', 'created_at')

admin.site.register(Plant, PlantAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Country)
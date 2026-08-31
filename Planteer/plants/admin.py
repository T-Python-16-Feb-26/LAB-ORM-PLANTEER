from django.contrib import admin

from .models import Plant, Comment, Country

class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'about','used_for','image', 'category', 'is_edible', 'created_at')
    list_filter = ('category', 'is_edible')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'plant', 'text', 'created_at')
    list_filter = ('plant', 'created_at')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'flag')
    

admin.site.register(Plant, PlantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Country, CountryAdmin)

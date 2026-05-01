from django.contrib import admin
from .models import Plant, Comment ,Country

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'flag')
    list_filter = ('name',)

class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_edible', 'created_at')
    list_filter = ('category', 'is_edible')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'plant', 'created_at')
    list_filter = ('plant', 'created_at')


# Register your models here.
admin.site.register(Plant, PlantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Country, CountryAdmin)

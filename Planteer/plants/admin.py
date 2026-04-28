from django.contrib import admin
from .models import Plant, Comment, Country, Publisher


class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_edible']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['plant', 'text', 'created_at']
    list_filter = ("plant",)


admin.site.register(Plant, PlantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Country)
admin.site.register(Publisher)
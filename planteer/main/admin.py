from django.contrib import admin
from .models import Contact
from plants.models import Plant, Comments, Country
from django.urls import path, include

# Register your models here.
class PlantAdmin(admin.ModelAdmin):
    list_display = ["name","category","is_edible","created_at"]
    list_filter = ("category", "is_edible")
    
class CommentsAdmin(admin.ModelAdmin):
    list_display = ["name", "plant", "created_at"]
    list_filter = ("plant","created_at")
    

class ContactAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "created_at"]

admin.site.register(Contact, ContactAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Plant, PlantAdmin)
admin.site.register(Country)
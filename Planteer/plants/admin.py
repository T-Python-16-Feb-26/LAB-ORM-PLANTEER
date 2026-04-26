from django.contrib import admin
from plants.models import Plant, Comment,Country

# Register your models here.

class PlantAdmin(admin.ModelAdmin):
    list_display=('name_plant','category')
    list_filter=['category']

class CommentAdmin(admin.ModelAdmin):
    list_display=('user','plant','created_at_comment')
    

admin.site.register(Plant,PlantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Country)


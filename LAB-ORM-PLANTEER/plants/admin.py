from django.contrib import admin
from .models import Plant, Comment, Country

admin.site.register(Plant)
admin.site.register(Comment)
admin.site.register(Country)
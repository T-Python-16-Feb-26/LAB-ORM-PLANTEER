from django.contrib import admin

# Register your models here.

from .models import Profile, Bookmark
admin.site.register(Profile)
admin.site.register(Bookmark)
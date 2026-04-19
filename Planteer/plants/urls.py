from django.urls import path
from . import views

app_name="plants"

urlpatterns=[
    path('new/', views.add_plant_view, name='add_plant_view')
]
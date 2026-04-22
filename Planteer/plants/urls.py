from django.urls import path
from . import views

app_name = "plants"

urlpatterns = [
    path('all/', views.all_plants, name='all_plants'),
    path('search/', views.search_plants, name='search'),
    path('new/', views.add_plant, name='add_plant'),
    path('<int:plant_id>/detail/', views.plant_detail, name='plant_detail'),
    path('<int:plant_id>/update/', views.update_plant, name='update_plant'),
    path('<int:plant_id>/delete/', views.delete_plant, name='delete_plant'),
    path('<int:plant_id>/add_review/', views.add_review, name='add_review'),
    path('country/<int:country_id>/', views.plants_by_country, name='plants_by_country'),
]
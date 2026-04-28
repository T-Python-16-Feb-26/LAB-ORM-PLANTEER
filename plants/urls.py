from django.urls import path
from . import views

app_name='plants'

urlpatterns = [
    path('all/', views.view_plants, name='view_plants'),
    path('plants/',views.plants_page,name='plants_page'),
    path('<int:plant_id>/detail/', views.plant_detail, name='plant_detail'),
    path('new/', views.plant_create, name='plant_create'),
    path('<int:plant_id>/update/', views.plant_update, name='plant_update'),
    path('<int:plant_id>/delete/', views.plant_delete, name='plant_delete'),
    path('search/', views.search_plants, name='search_plants'),
    path('find/', views.find_plant, name='find_plant'),
    path('countries/<int:country_id>/',views.country_plants,name='country_plants'),
]
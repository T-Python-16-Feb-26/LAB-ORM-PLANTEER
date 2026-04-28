from django.urls import path
from . import views



urlpatterns = [
    path('all/', views.all_plants, name='all_plants'),
    path('<int:plant_id>/detail/', views.plant_detail, name='plant_detail'),
    path('new/', views.add_plant, name='add_plant'),
    path('<int:plant_id>/update/', views.update_plant, name='update_plant'),
    path('<int:plant_id>/delete/', views.delete_plant, name='delete_plant'),
    path('search/', views.search_plants, name='search_plants'),
    path('<int:plant_id>/comment/', views.add_comment, name='add_comment'),
    path('country/<int:country_id>/', views.plants_by_country, name='plants_by_country'),
    path('publisher/<int:publisher_id>/', views.plants_by_publisher, name='plants_by_publisher'),
    path('publishers/', views.publishers_list, name='publishers_list'),
    
    
    
]
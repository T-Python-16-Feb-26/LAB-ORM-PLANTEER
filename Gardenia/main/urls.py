from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    # Home
    path('', views.home_view, name='home'),

    # Plants
    path('plants/all/', views.all_plants_view, name='all_plants'),
    path('plants/<int:id>/detail/', views.plant_detail_view, name='plant_detail'),

    # Search
    path('plants/search/', views.search_view, name='search'),
    
    # Contact
    path('contact/', views.contact_view, name='contact'),
    path('contact/messages/', views.messages_view, name='messages'),
    
     # CRUD
    path('plants/new/', views.add_plant_view, name='add_plant'),
    path('plants/<int:id>/update/', views.update_plant_view, name='update_plant'),
    path('plants/<int:id>/delete/', views.delete_plant_view, name='delete_plant'),

]

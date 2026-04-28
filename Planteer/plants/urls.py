from django.urls import path
from . import views


app_name = "plants"

urlpatterns = [
    path('new/', views.add_plant_view, name='add_plant_view'),
    path('search/', views.search_plants_view, name='search_plants_view'),
    path('<str:category_name>/', views.all_plants_view, name='all_plants_view'),
    path('detail/<int:plant_id>/', views.plant_detail_view, name='plant_detail_view'),
    path("update/<int:plant_id>/", views.plant_update_view, name="plant_update_view"),
    path("delete/<int:plant_id>/", views.plant_delete_view, name="plant_delete_view"),
]
from django.urls import path
from . import views

app_name = "plant"
urlpatterns = [
    path('all/', views.plants_view, name="plants_view"),
    path('new/', views.new_plant_view, name="new_plant_view"),
    path('<plant_id>/update/', views.update_plant_view, name="update_plant_view"),
    path('<plant_id>/detail/', views.detail_plant_view, name="detail_plant_view"),
    path('<plant_id>/delete/', views.delete_plant_view, name="delete_plant_view"),
    path('search/', views.search_plant_view, name="search_plant_view"),
    path('<plant_id>/add_comment/', views.add_comment_view, name="add_comment_view"),
]
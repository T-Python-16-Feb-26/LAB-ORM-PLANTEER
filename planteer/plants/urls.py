from django.urls import path
from . import views

#Plant Detail Page : plants/<plant_id>/detail/
# Add new plant page : plants/new/
# Update plant page : plants/<plant_id>/update/,
# Delete Plant : plants/<plant_id>/delete/
# Search Page : plants/search/
app_name = "plants"

urlpatterns = [
    path('all/', views.all_plants_view, name="all_plants_view"),
    path('<int:plant_id>/', views.plant_detail_view, name="plant_detail_view"),
    path('search/', views.search_view, name="search_view"),
    path('new/', views.create_view, name="create_view"),
    path('<int:plant_id>/edit', views.update_view, name="update_view"),
    path('<int:plant_id>/delete', views.delete_view, name="delete_view"),
    path('<int:plant_id>/comment', views.comment_create_view, name="comment_create_view"),


]
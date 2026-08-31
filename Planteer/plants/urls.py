from django.urls import path
from . import views

app_name = 'plants'

urlpatterns = [
    path('all/', views.all_plant_view, name='all_plant_view'),
    path('<int:plant_id>/detail/', views.plant_detail_view, name='plant_detail_view'),
    path('new/', views.add_plant_view, name='add_plant_view'),
    path('<int:plant_id>/update/', views.update_plant_view, name='update_plant_view'),
    path('<int:plant_id>/delete/', views.delete_plant_view, name='delete_plant_view'),
    path('search/', views.search_plant_view, name='search_plant_view'),
    path('comments/add/<int:plant_id>/', views.add_comment_view, name='add_comment_view'),
    path('comments/<int:comment_id>/delete/', views.delete_comment_view, name='delete_comment_view'),
    path('country/<int:country_id>/', views.plants_by_country_view, name='plants_by_country_view'),
]
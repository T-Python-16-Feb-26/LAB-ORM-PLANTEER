from django.urls import path
from . import views

app_name="plants"

urlpatterns=[
    path('new/', views.add_plant_view, name='add_plant_view'),
    path('<plant_id>/detail/', views.plant_detail_view, name='plant_detail_view'),
    path('<plant_id>/update/', views.plant_update_view, name='plant_update_view'),
    path('plants/<plant_id>/delete/', views.plant_delete_view, name='plant_delete_view'),
    path('all/' , views.all_plants_view, name='all_plants_view'),
    path('search/', views.search_plants_view, name='search_plant_view'),
    path('comment/add/<plant_id>', views.add_comment_view,name='add_comment_view'),
]
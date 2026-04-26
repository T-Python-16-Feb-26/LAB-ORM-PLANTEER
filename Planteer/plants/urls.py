from django.urls import path
from . import views

app_name = "plants"

urlpatterns= [

    path("all/", views.all_plants_view, name="all_plants_view"),
    path("<int:plant_id>/detail/", views.plant_detail_view, name="plant_detail_view"),
    path("new/", views.add_plant_view, name="add_plant_view"),
    path("<int:plant_id>/update/", views.update_plant_view, name="update_plant_view"),
    path("<int:plant_id>/delete/", views.delete_plant_view, name="delete_plant_view"),
    path("search/", views.search_view, name="search_view"),
    path("review/add/<plant_id>/", views.add_review_view, name="add_review_view"),
    path('country/<country_id>/', views.country_plants_view, name='country_plants_view'),
]

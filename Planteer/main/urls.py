from django.urls import path
from . import views


app_name = "main"

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('base/', views.base_view, name="base_view"),
    path('contact/', views.contact_view, name="contact_view"),
    path('contact/messages/', views.contact_messages_view, name="contact_messages_view"),
    path("mode/<mode>/", views.mode_view, name="mode_view"),
]
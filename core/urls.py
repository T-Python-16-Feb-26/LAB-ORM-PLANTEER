from django.urls import path
from . import views

app_name='core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/messages/', views.contact_messages_view, name='contact_messages'),
    path('services/', views.services_view, name='services'),
    path("register/", views.register_view, name="register"),
    path("accounts/logout/", views.logout_view, name="logout"),

    
]
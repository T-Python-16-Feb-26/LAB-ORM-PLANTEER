from django.urls import path
from . import views

app_name="main"

urlpatterns=[
    path("", views.home_view, name="home_view"),
    path("contact/" , views.Contact_us_view, name="Contact_us_view"),
    path("contact/messages/", views.message_view, name="message_view"),
    ]
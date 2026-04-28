from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name='home'),

    path('contact/', views.contact, name='contact'),

    path('messages/', views.messages_view, name='messages'),

    path('toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),

    path('care-tips/', views.care_tips_view, name='care_tips'),

    path('care-tips/<str:slug>/', views.article_view, name='article'),

    path('find-my-plant/', views.find_my_plant_view, name='find_my_plant'),

    path('find-my-plant/results/', views.find_my_plant_results, name='find_my_plant_results'),

    path('favourites/', views.favourites_view, name='favourites'),

    path('register/', views.register_view, name='register'),

    path('login/', views.login_view, name='login'),
    
    path('logout/', views.logout_view, name='logout'),

]
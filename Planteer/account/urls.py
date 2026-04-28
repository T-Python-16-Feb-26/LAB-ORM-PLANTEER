from django.urls import path
from . import views

app_name="account"

urlpatterns=[
    path('sign-up/', views.sign_up_view, name="sign_up_view"),
    path('sign-in/', views.sign_in_view, name="sign_in_view"),
    path('log-out/', views.log_out_view, name="log_out_view"),
    path('profile/', views.profile_view, name='profile_view')
]
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.sign_up_view, name="sign_up"),
    path('login/', views.sign_in_view, name="log_in"),
    path('logout/', views.log_out, name="log_out"),
    path('profile/<str:user_id>/', views.profile_view, name="profile_view"),
]
#accounts:log_in
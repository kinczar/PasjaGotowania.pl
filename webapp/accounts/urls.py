from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/<int:user_id>/', views.profile, name='user_profile'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
]
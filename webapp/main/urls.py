# Plik do zarządzania ścieżkami w aplikacji. Zawiera listę ścieżek powiązanych z widokami.

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('cars', views.cars, name='cars'),
    path('recipes', views.recipes, name='recipes'),
    path('recipes/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/favorite/<int:id>/', views.toggle_favorite, name='toggle_favorite'),

    path('login', views.login_user, name='login_user'),
    path('register', views.register, name='register_user'),
    path('logout', views.logout_user, name='logout_user'),

    path('health/', views.health, name='health'),
]

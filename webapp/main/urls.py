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

    path('login', views.login_user, name='login_user'),
    path('register', views.register, name='register_user'),
    path('logout', views.logout_user, name='logout_user'),

    # 👇 TO DODAŁEŚ (twoja nowa podstrona)
    path('health/', views.health, name='health'),
<<<<<<< Updated upstream
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    path("post/<int:id>/", views.post_detail, name="detail"),


    path('calculate-bmi/', views.calculate_bmi),
    path('calculate-calories/', views.calculate_calories),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> Stashed changes

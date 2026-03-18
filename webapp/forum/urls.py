from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
    path('index/', views.index),
    path('frequent_questions/', views.frequent_questions),
    path('add/', views.add_post, name='add_post'),
     path('delete/<int:post_id>/', views.delete_post, name='delete_post'), #usuwanie postu
]
 

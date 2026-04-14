from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
    path('index/', views.index),
    path('frequent_questions/', views.frequent_questions),
    path('add/', views.add_post, name='add_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'), #usuwanie postu
    path('like/<int:post_id>/', views.like_post, name='like_post'), #dodawnaie like do posta
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'), #komentarze
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'), #like komentarza
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'), #usuwanie komentarza
    path('save/<int:post_id>/', views.toggle_save, name='toggle_save'), #zapisywanie posta
    
]
 

from django.urls import path,include
from . import views

urlpatterns = [
    path('posts', views.Posts.as_view()),
    path('post', views.Post.as_view()),




]


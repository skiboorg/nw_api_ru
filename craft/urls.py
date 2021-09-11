from django.urls import path,include
from . import views

urlpatterns = [
    path('categories', views.GetCategories.as_view()),
    path('recipes', views.GetRecipes.as_view()),
    path('recipe/<int:pk>', views.GetRecipe.as_view()),
    # path('post', views.Post.as_view()),




]


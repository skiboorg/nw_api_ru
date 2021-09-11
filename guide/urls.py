from django.urls import path,include
from . import views

urlpatterns = [
    path('guides', views.GetGuides.as_view()),
    path('guide', views.GetGuide.as_view()),



]


from django.urls import path,include
from . import views

urlpatterns = [
    path('guilds', views.GetGuilds.as_view()),
    path('guild', views.GetGuild.as_view()),
    path('create', views.CreateGuild.as_view()),
    path('feedback', views.Feedback.as_view()),


]


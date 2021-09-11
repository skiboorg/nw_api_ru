from django.urls import path,include
from . import views

urlpatterns = [
    path('event', views.EventAction.as_view()),
    path('events', views.Events.as_view()),
    path('events_full', views.EventsFull.as_view()),
    path('event_action', views.EventUser.as_view()),
    path('event_user', views.EventUserAction.as_view()),
    path('add_users', views.AddUsers.as_view()),




]


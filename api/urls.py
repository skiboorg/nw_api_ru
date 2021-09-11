from django.urls import path,include
from . import views

urlpatterns = [
    path('items', views.Item.as_view()),
    path('cc', views.Craft.as_view()),

    path('banner', views.GetBanner.as_view()),
    path('faq', views.GetFaq.as_view()),
    path('social', views.GetSocial.as_view()),
    path('add_fb', views.AddFb.as_view()),
    path('texts', views.GetTexts.as_view()),



]


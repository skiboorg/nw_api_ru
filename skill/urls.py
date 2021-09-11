from django.urls import path,include
from . import views

urlpatterns = [
    path('weapons', views.GetWeapons.as_view()),
    path('weapon', views.GetWeapon.as_view()),
    path('characteristics', views.GetCharacteristics.as_view()),

    path('build', views.Builds.as_view()),
    path('feedback', views.AddFeedback.as_view()),
    path('builds_filter', views.BuildsFilter.as_view()),
    #path('builds_correct', views.BuildsCorrect.as_view()),

    # path('parse', views.ParceHtml.as_view()),



]


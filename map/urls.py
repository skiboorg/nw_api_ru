from django.urls import path,include
from . import views

urlpatterns = [
    path('poi', views.GetPoi.as_view()),
    path('resourse', views.GetResourse.as_view()),

    # path('parse_poi', views.ParcePoi.as_view()),
    # path('parse_res', views.ParceResource.as_view()),
    # path('get_map', views.ParceMap.as_view())

]


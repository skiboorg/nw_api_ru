from django.urls import path,include
from . import views

urlpatterns = [
    # path('get_items', views.ParseItems.as_view()),
    path('category', views.GetCategory.as_view()),
    path('subcategory', views.GetSubCategory.as_view()),
    path('items', views.GetItems.as_view()),
    path('item', views.GetItem.as_view()),
    # path('del', views.Del.as_view()),





]


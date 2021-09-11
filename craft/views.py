import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *


class GetCategories(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class GetRecipes(generics.ListAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

class GetRecipe(generics.RetrieveAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.filter()

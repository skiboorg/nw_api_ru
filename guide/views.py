from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *

class GetGuides(generics.ListAPIView):
    serializer_class = GuideCategorySerializer
    queryset = GuideCategory.objects.all()

class GetGuide(generics.RetrieveAPIView):
    serializer_class = GuideSerializer

    def get_object(self):
        try:
            item = Guide.objects.filter(name_slug=self.request.query_params.get('slug'))[0]
        except:
            item = Guide.objects.filter(name_slug=self.request.query_params.get('slug'))
        return item


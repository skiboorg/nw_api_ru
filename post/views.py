from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *

class Posts(generics.ListAPIView):
    serializer_class = PostsSerializer

    def get_queryset(self):
        requestType = self.request.query_params.get('for')
        if requestType == 'index':
            return PostItem.objects.filter(is_active=True)[:5]
        if requestType == 'all':
            return PostItem.objects.filter(is_active=True)


class Post(generics.RetrieveAPIView):
    serializer_class = PostSerializer

    def get_object(self):
        try:
            item = PostItem.objects.filter(name_slug=self.request.query_params.get('slug'))[0]
        except:
            item = PostItem.objects.filter(name_slug=self.request.query_params.get('slug'))
        return item


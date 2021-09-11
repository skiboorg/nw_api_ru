import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *

class GetGuilds(generics.ListAPIView):
    serializer_class = GuildsSerializer

    def get_queryset(self):
        requestType = self.request.query_params.get('for')
        if requestType == 'index':
            return Guild.objects.filter(is_active=True)[:3]
        if requestType == 'all':
            return Guild.objects.filter(is_active=True)


class GetGuild(generics.RetrieveAPIView):
    serializer_class = GuildSerializer

    def get_object(self):
        try:
            item = Guild.objects.filter(name_slug=self.request.query_params.get('slug'))[0]
        except:
            item = Guild.objects.filter(name_slug=self.request.query_params.get('slug'))
        return item

class CreateGuild(APIView):
    def post(self,request):
        data=json.loads(request.data.get('data'))
        img=request.data.get('img')
        guild = Guild.objects.create(
            name=data['name'],
            fraction=data['fraction'],
            server=data['server'],
            size=data['size'],
            style=data['style'],
            description=data['description'],
            discord_link=data['discord_link']
        )
        if img:
            guild.image = img
            guild.save()
        return Response(status=200)

class Feedback(APIView):
    def get(self, request):
        q = GuildFeedback.objects.filter(guild__name_slug=self.request.query_params.get('slug'),is_active=True)
        serializer = GuildFeedbackSerializer(q, many=True)
        return Response(serializer.data, status=200)
    def post(self, request):
        data = request.data
        print(data)
        guild = Guild.objects.get(id=data['guild_id'])
        GuildFeedback.objects.create(
            user=request.user,
            guild=guild,
            text=request.data.get('text'),
            rating=request.data.get('rating')
        )
        return Response(status=200)
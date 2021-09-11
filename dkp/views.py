from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *

class Events(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.filter(is_active=True)

class EventsFull(generics.ListAPIView):
    serializer_class = EventFullSerializer
    queryset = Event.objects.all()

class EventUserAction(APIView):
    def post(self,request):
        data = request.data
        print(data)
        event = Event.objects.get(id=data['event_id'])
        event_user = EventDkp.objects.get(id=data['player_id'])
        if data['action'] == 'save':
            event_user.amount = int(data['amount'])
            event_user.save()
        else:
            event_user.delete()
        return Response(status=200)

def calcDkp(event):
    players = event.players.all()
    print(event.dpk_points)
    print(event.players_count)
    for p in players:
        p.amount = event.dpk_points / event.players_count
        p.save()

class EventUser(APIView):
    def post(self,request):
        data = request.data
        print(data)
        event = Event.objects.get(id=data['event_id'])
        if data['action'] == 'add':
            event.players_count += 1
            event.save()
            EventDkp.objects.create(event=event,player=request.user)
            calcDkp(event=event)
        else:
            eventObj = EventDkp.objects.get(event=event,player=request.user)
            eventObj.delete()
            event.players_count -= 1
            event.save()
            calcDkp(event=event)
        return Response(status=200)

class AddUsers(APIView):
    def post(self, request):
        data = request.data
        event = Event.objects.get(id=data['event_id'])
        users = data['add_users']
        for user in users:
            event.players_count += 1
            event.save()
            EventDkp.objects.create(event=event, player_id=int(user['id']))
        calcDkp(event=event)
        return Response(status=200)

class EventAction(APIView):
    def post(self,request):
        data = request.data
        print(data)
        Event.objects.create(
            name=data['name'],
            description=data['description'],
            date=data['date'].replace('/','-'),
            time=data['time'],
            code=data['code'],
            dpk_points=data['dpk_points'],
        )
        return  Response(status=200)
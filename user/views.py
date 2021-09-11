import json
import uuid

from django.http import HttpResponseRedirect


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .models import *
from rest_framework import generics




class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print(request.data)


        serializer = UserSerializer(user, data=request.data['userData'])
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            print(serializer.errors)
            return Response(status=400)

class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    print(serializer_class.data)
    def get_object(self):
        return self.request.user
    # def get(self, request):
    #     user = request.user
    #     serializer = UserSerializer(user, many=False)
    #     return Response(serializer.data)


class UserRecoverPassword(APIView):
    def post(self,request):
        user = None
        try:
            user = User.objects.get(phone=request.data['phone'])
        except:
            user = None
        if user:
            messageSend = True
            return Response({'result': True, 'email': user.email}, status=200)
        else:
            return Response({'result': False}, status=200)


class GetMembers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_guild_member=True)



# class ChangePassword(APIView):
#     def post(self, request):
#         print(request.data)
#         user = User.objects.get(phone = request.data['phone'])
#         result = send_sms(user.phone, True, 'Ваш новый пароль : ')
#         user.set_password(result['code'])
#         user.save()
#         return Response(status=200)
#
#
#
# class SendCodeSMS(APIView):
#     def post(self, request):
#         print(request.data)
#         phone = request.data.get('phone')
#         result = send_sms(phone,True)
#
#         return Response(result,status=200)







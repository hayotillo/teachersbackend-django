from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class UserView(RetrieveAPIView):
    model = User
    serializer_class = UserSerializers
    queryset = User.objects.all()

    def retrieve(self, request, pk=None):
        if request.user and pk == 'me':
            return JsonResponse(UserSerializers(request.user).data)
        return super(UserView, self).retrieve(request, pk)


# logout
class LogoutView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

from django.shortcuts import render
from django.http import JsonResponse
# from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
# User = get_user_model()


class DataView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_data(self, request, **kwargs):
        data_type = kwargs.get('data_type')
        if data_type == 'main':
            user_account = UserAccount.objects.filter(user__id=request.user.id).first()
            if user_account:
                serializer = UserAccountSerializer(instance=user_account, many=False)
                return JsonResponse(serializer.data)
            else:
                return JsonResponse({'error': 'user not fount!'})
        else:
            return JsonResponse({'error': 'data type not fount!'})


class SaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        user_account = UserAccount.objects.filter(user__id=request.user.id).first()
        if user_account:
            serializer = UserAccountSerializer(instance=user_account, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            else:
                return JsonResponse({'error': 'user not fount!'})
        else:
            return JsonResponse({'error': 'data type not fount!'})


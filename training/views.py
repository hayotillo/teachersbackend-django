from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *


class DataView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_data(self, request, **kwargs):
        data_type = kwargs.get('data_type')
        if data_type == 'main':
            training = Training.objects.filter(user__id=request.user.id).first()
            serializer = TrainingAccountSerializer(instance=training, many=False)
            return JsonResponse(serializer.data)

        else:
            return JsonResponse({'error': 'data type not fount!'})


class SaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        training_account = Training.objects.filter(user__id=request.user.id).first()
        if training_account:
            serializer = TrainingAccountSerializer(instance=training_account, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            else:
                return JsonResponse({'error': 'user not fount!'})
        else:
            return JsonResponse({'error': 'data type not fount!'})

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .serializers import *

User = get_user_model()


class Logout(APIView):

    def get(self, request, **kwargs):
        request.user.auth_token.delete()
        logout(request)

        return JsonResponse({'is_logout': True})


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            i = 1
            errors = []
            for field, messages in serializer.errors.items():
                for message in messages:
                    field_name = ''
                    if field == 'password':
                        field_name = 'Parol'
                    if field == 'password2':
                        field_name = 'Parolni qaytarish'
                    elif field == 'username':
                        field_name = 'Login'
                    elif field == 'email':
                        field_name = "Elekton po'chta"
                    elif field == 'first_name':
                        field_name = "Ism"
                    elif field == 'last_name':
                        field_name = "Familiya"
                    else:
                        field_name = field
                    errors.append(f'{str(i)}: {field_name} - {message}')
                    i += 1
            return JsonResponse({'errors': errors})


class DataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        user = User.objects.filter(pk=request.user.id).first()
        if user:
            serializer = UserSerializer(instance=user, many=False)
            return JsonResponse(serializer.data)
        else:
            return JsonResponse({'error': 'user not fount'})


class UpdateUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        user = User.objects.filter(pk=request.user.id).first()
        if user:
            serializer = UserManageSerializer(instance=user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            else:
                return JsonResponse(serializer.errors)


class AuthTokenLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key})


class ShortData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = User.objects.filter(pk=request.user.id).first()
        serializer = UserShortSerializer(queryset, many=False)
        return JsonResponse(serializer.data)


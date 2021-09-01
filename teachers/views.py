from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import *
from .models import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


# vote
class VoteView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    model = None
    like_type = None

    def like(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.model = kwargs.get('model')
        query_type = kwargs.get('like_type')
        if query_type == 'like':
            self.like_type = Vote.LIKE
        elif query_type == 'dislike':
            self.like_type = Vote.DISLIKE

        obj = self.model.objects.get(pk=pk)
        try:
            user = User.objects.get(pk=request.user.id)
            like = Vote.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                user=user
            )

            if like.vote is not self.like_type:
                like.vote = self.like_type
                like.save(update_fields=['vote'])
                result = True
            else:
                like.delete()
                result = False

        except Vote.DoesNotExist:
            obj.vote.create(user=user, vote=self.like_type)
            result = True

        return JsonResponse({
            "result": result,
            "like_count": obj.vote.likes().count(),
            "dislike_count": obj.vote.dislikes().count(),
            "sum_rating": obj.vote.sum_rating()
        })


# teacher
class TeacherView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializers

    def get_queryset(self):
        print(self.kwargs)
    # def list(self, request, **kwargs):
    #     page = int(kwargs.get('page'))
    #     if page > 0:
    #         pass
    #     # teachers = Teacher.objects.all()
    #     return JsonResponse({'teachers': self.queryset.all()})

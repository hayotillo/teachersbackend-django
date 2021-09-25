from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from teachers.models import Teacher
from training.models import Training


class StandardResultsSetPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return JsonResponse({
            'paginator': {
                'has_next_page': self.page.has_next(),
                'current_page': self.page.number,
                'page_count': self.page.paginator.num_pages,
                'total': self.page.paginator.count
            },
            'results': data
        })


class ListView(ListAPIView):
    pass


class DataManageView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def save(self, request, **kwargs):
        object_id = request.data.get('object_id')
        model_name = request.data.get('model_name')

        if object_id and model_name:
            course = Course.objects.filter(pk=request.data.get('id')).first()
            serializer = CourseSerializer(instance=course, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            else:
                return JsonResponse(serializer.errors)

        else:
            return JsonResponse({'error': 'object id or model name not got!'})

    def delete(self, request, **kwargs):
        object_id = request.data.get('object_id')
        model_name = request.data.get('model_name')

        if object_id and model_name:
            model_name = request.data.get('model_name')
            if model_name == 'teacher':
                model = Teacher.objects.filter(pk=object_id).first()
            elif model_name == 'training':
                model = Training.objects.filter(pk=object_id).first()

            model = model.courses.filter(pk=object_id).first()
            if model:
                model.delete()
                return JsonResponse({'result': True})
            else:
                return JsonResponse({'error': 'this course not fount!'})

        else:
            return JsonResponse({'error': 'object id or model name not got!'})


class DetailView(viewsets.ModelViewSet):
    pass

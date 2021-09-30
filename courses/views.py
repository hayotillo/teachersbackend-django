from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, **kwargs):
        model_name = kwargs.get('model_name')
        object_id = kwargs.get('object_id')
        return get_paginate_list(request=request, model_name=model_name, object_id=object_id)


class ListAllView(ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        queryset = Course.objects.filter(status='active').order_by('start_time')
        pagination_class = StandardResultsSetPagination
        paginator = pagination_class()
        page = paginator.paginate_queryset(queryset=queryset, request=request)
        serializer = CourseSerializer(instance=page, many=True)
        return paginator.get_paginated_response(data=serializer.data)


class DataManageView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def save(self, request, **kwargs):
        model_name = request.data.get('model_name')

        if model_name:
            user_id = request.user.id
            if model_name == 'teacher':
                model = Teacher.objects.filter(user_id=user_id).first()
            elif model_name == 'training':
                model = Training.objects.filter(user_id=user_id).first()

            course = model.courses.filter(pk=request.data.get('id')).first()
            data = request.data.copy()
            data.update({'object_id': model.id})

            serializer = CourseSerializer(instance=course, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # return JsonResponse(serializer.data)
                return get_paginate_list(request=request, model_name=model_name)
            else:
                return JsonResponse(serializer.errors)

        else:
            return JsonResponse({'error': 'object id or model name not got!'})

    def delete(self, request, **kwargs):
        user_id = request.user.id
        model_name = kwargs.get('model_name')

        if user_id and model_name:
            if model_name == 'teacher':
                model = Teacher.objects.filter(user_id=user_id).first()
            elif model_name == 'training':
                model = Training.objects.filter(user_id=user_id).first()

            model = model.courses.filter(pk=kwargs.get('pk')).first()
            if model:
                model.delete()
                return JsonResponse({'result': True})
            else:
                return JsonResponse({'error': 'this course not fount!'})

        else:
            return JsonResponse({'error': 'object id or model name not got!'})


class DetailView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_detail(self, request, **kwargs):
        instance = Course.objects.filter(pk=kwargs.get('pk')).first()
        serializer = CourseSerializer(instance=instance, many=False)
        return JsonResponse(serializer.data)


def get_paginate_list(request, model_name, object_id='fcu'):
    if object_id == 'fcu':
        object_id = request.user.id

    model = None
    if model_name == 'teacher':
        model = Teacher.objects.filter(status='active', user_id=object_id).first()

    elif model_name == 'training':
        model = Training.objects.filter(status='active', user_id=object_id).first()

    if model:
        content_type = ContentType.objects.get_for_model(model=model)
        queryset = Course.objects.filter(status='active', object_id=model.id, content_type=content_type)

    if queryset:
        queryset = queryset.order_by('start_time')
        pagination_class = StandardResultsSetPagination
        paginator = pagination_class()
        page = paginator.paginate_queryset(queryset=queryset, request=request)
        serializer = CourseSerializer(instance=page, many=True)
        return paginator.get_paginated_response(data=serializer.data)
    else:
        return JsonResponse({'result': 'course not fount!'})

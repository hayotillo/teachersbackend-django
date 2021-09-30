from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class StandardResultsSetPagination(PageNumberPagination):
    # page_size = 20
    # page_size_query_param = 'page_size'
    # max_page_size = 15

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
    pagination_class = StandardResultsSetPagination
    paginator = pagination_class()

    def get(self, request, **kwargs):
        queryset = Book.objects.filter(status='published').order_by('-created_at')
        page = self.paginator.paginate_queryset(queryset=queryset, request=request)
        serializer = BookListSerializer(instance=page, many=True)
        return self.paginator.get_paginated_response(data=serializer.data)


class DetailView(ModelViewSet):

    permission_classes = [AllowAny]

    def get_detail(self, request, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            queryset = Book.objects.filter(pk=pk).first()
            serializer = BookDetailSerializer(instance=queryset, many=False)
            return JsonResponse(serializer.data)

        return JsonResponse({'error': 'book not fount'})

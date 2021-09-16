from rest_framework import viewsets
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from .models import *


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


# teacher account
class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)

        return JsonResponse({'result': True})


class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        serializer = TeacherRegisterSerializer(data=request.data)
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


class ManageTeacherAccount(APIView):
    def post(self, request, **kwargs):
        teacher = Teacher.objects.filter(pk=request.user.id).first()
        if teacher:
            serializer = TeacherManageSerializer(teacher, data=request.data, many=False, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            else:
                return JsonResponse({'errors': serializer.errors})


class TeacherObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(TeacherObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return JsonResponse({'token': token.key})


# teacher
class TeacherListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # pagination_class = LargeResultsSetPagination
    pagination_class = StandardResultsSetPagination
    paginator = pagination_class()

    # queryset = Teacher.objects.filter(status='active')
    serializer_class = TeacherListSerializer

    def get(self, request, *args, **kwargs):
        queryset = Teacher.objects.filter(status='active')
        page = self.paginator.paginate_queryset(queryset, request)
        serializer = TeacherListSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class TeacherView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Teacher.objects.filter(status='active')
    serializer_class = TeacherListSerializer

    def check_token(self, request):
        return JsonResponse({'is_login': request.user.is_authenticated})

    def teacher(self, request, **kwargs):
        pk = kwargs.get('pk')
        if pk == 'me':
            teacher = self.queryset.filter(user__pk=request.user.id)
        else:
            teacher = self.queryset.filter(pk=int(pk))
        serialize_teacher = TeacherDetailSerializer(teacher, many=True)
        if serialize_teacher.data:
            return JsonResponse(serialize_teacher.data[0], safe=False)
        return JsonResponse({})


class ManageDataView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    # save data form
    def save(self, request, **kwargs):
        if request.user.is_authenticated:
            serializer = None
            teacher = Teacher.objects.filter(user__id=request.user.id).first()
            data_type = kwargs.get('data_type')

            if data_type == 'main':
                serializer = TeacherSerializer(teacher, data=request.data, partial=True)
                if request.data.get('delete_photo', False):
                    teacher.photo.delete(save=True)

            elif data_type == 'location':
                serializer = TeacherSerializer(teacher, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'result': True})
                else:
                    return JsonResponse(serializer.errors)

            elif data_type == 'portfolio':
                portfolio = teacher.portfolios.filter(pk=request.data.get('id')).first()
                if portfolio is None:
                    portfolio = teacher.portfolios.create()
                # return JsonResponse({'result': 'ok'})
                serializer = PortfolioSerializer(portfolio, data=request.data, partial=True)

            elif data_type == 'workplace':
                workplace = teacher.workplaces.filter(pk=request.data.get('id')).first()
                if workplace is None:
                    workplace = teacher.workplaces.create(start_date=request.data.get('start_date'))

                serializer = WorkplaceSerializer(workplace, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()

                    queryset = teacher.workplaces.all()
                    page = self.paginator.paginate_queryset(queryset, request)
                    serializer = WorkplaceSerializer(page, many=True)
                    # return JsonResponse({
                    #     'teacher_id': teacher.id,
                    #     'workplaces_data': serializer.data
                    # })
                    return self.paginator.get_paginated_response(serializer.data)
                else:
                    return JsonResponse(serializer.errors)

            elif data_type == 'account':
                serializer = TeacherManageSerializer(teacher, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    serializer = TeacherAccountSerializer(teacher, many=False)
                    return JsonResponse(serializer.data)
                else:
                    return JsonResponse(serializer.errors)

            else:
                return JsonResponse({'error': 'type not fount!'}, status=500)

            if serializer is not None:
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data)
                else:
                    return JsonResponse(serializer.errors)

        else:
            return JsonResponse({'error': 'teacher id not fount!'}, status=500)

    def delete(self, request, **kwargs):
        if request.user.is_authenticated:
            teacher = Teacher.objects.filter(user__id=request.user.id).first()
            pk = kwargs.get('pk')
            if pk:
                data_type = kwargs.get('data_type')
                if data_type == 'portfolio':
                    portfolio = teacher.portfolios.filter(pk=pk).first()
                    if portfolio:
                        portfolio.delete()

                elif data_type == 'workplace':
                    career = teacher.workplaces.get(pk=pk)
                    if career:
                        career.delete()

                else:
                    return JsonResponse({'error': 'type not fount!'}, status=500)

                return JsonResponse({'result': True})

            else:
                return JsonResponse({'error': 'item id not fount!'}, status=500)

        else:
            return JsonResponse({'error': 'teacher id not fount!'}, status=500)


class DataView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    paginator = pagination_class()

    # get teacher data by filter
    def get(self, request, *args, **kwargs):
        data_filter = kwargs.get('data_filter')
        teacher = Teacher.objects.filter(user__id=request.user.id).first()
        if data_filter:
            if data_filter == 'main':
                queryset = Teacher.objects.filter(user__id=request.user.id).first()
                serializer = TeacherSerializer(queryset, many=False)
                return JsonResponse(serializer.data)

            elif data_filter == 'location':
                locations = Location.objects.all()
                districts = District.objects.all()
                regions = Region.objects.all()
                serializer_location = LocationSerializer(teacher.location, many=False)
                serializer_locations = LocationSerializer(locations, many=True)
                serializer_districts = DistrictSerializer(districts, many=True)
                serializer_regions = RegionSerializer(regions, many=True)
                serializer_data = {
                    'location': serializer_location.data,
                    'locations_data': serializer_locations.data,
                    'districts_data': serializer_districts.data,
                    'regions_data': serializer_regions.data
                }
                return JsonResponse(serializer_data)

            elif data_filter == 'portfolio':
                queryset = Portfolio.objects.filter(teacher__user__id=request.user.id)
                page = self.paginator.paginate_queryset(queryset, request)
                serializer = PortfolioSerializer(page, many=True)

            elif data_filter == 'workplace':
                queryset = Workplace.objects.filter(teacher__user__id=request.user.id)
                page = self.paginator.paginate_queryset(queryset, request)
                serializer = WorkplaceSerializer(page, many=True)
                if len(serializer.data) == 0:
                    return JsonResponse({'teacher_id': teacher.id})

            elif data_filter == 'account':
                serializer = TeacherAccountSerializer(teacher, many=False)
                return JsonResponse(serializer.data)

            if serializer:
                return self.paginator.get_paginated_response(serializer.data)
            else:
                return JsonResponse(None, status=404)
        else:
            return JsonResponse({'result': 'data filter not fount'}, status=500)


class ShortData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Teacher.objects.filter(user__id=request.user.id).first()
        serializer = TeacherShortSerializer(queryset, many=False)
        return JsonResponse(serializer.data)

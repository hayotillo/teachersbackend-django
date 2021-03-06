from rest_framework import viewsets
from django.http import JsonResponse
from django.contrib.auth import logout
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
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
class Logout(ObtainAuthToken):

    def get(self, request, format=None):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)

        return JsonResponse({'result': True})


class TeacherLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(TeacherLogin, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return JsonResponse({'token': token.key})


# teacher
class TeacherListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    paginator = pagination_class()

    # queryset = Teacher.objects.filter(status='active')
    serializer_class = TeacherListSerializer

    def get(self, request, *args, **kwargs):
        is_coach = request.query_params.get('is_coach') == 'true'
        print(request.query_params.get('is_coach'))
        print(is_coach)
        queryset = Teacher.objects.filter(
            status='active',
            is_coach=is_coach
        ).order_by('-user__last_login')
        page = self.paginator.paginate_queryset(queryset, request)
        serializer = TeacherListSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class TeacherView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Teacher.objects.filter(status='active')
    serializer_class = TeacherListSerializer

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
                    return self.paginator.get_paginated_response(serializer.data)
                else:
                    return JsonResponse(serializer.errors)

            elif data_type == 'account':
                if request.data.get('is_user'):
                    user = User.objects.filter(pk=request.user.id).first()
                    serializer = TeacherAccountSerializer(instance=user, data=request.data, partial=True)
                else:
                    serializer = TeacherManageSerializer(teacher, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()

                    if not request.data.get('is_user'):
                        serializer = TeacherAccountSerializer(teacher, many=False)

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
                            elif field == 'sur_name':
                                field_name = "Familiya"
                            else:
                                field_name = field
                            errors.append(f'{str(i)}: {field_name} - {message}')
                            i += 1
                    return JsonResponse({'errors': errors})

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
        if request.user.user_type == 'teacher':
            data_filter = kwargs.get('data_filter')
            teacher = Teacher.objects.filter(user__id=request.user.id).first()

            if teacher and data_filter:
                if data_filter == 'main':
                    serializer = TeacherSerializer(teacher, many=False)
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

                if serializer is not None:
                    return self.paginator.get_paginated_response(serializer.data)
                else:
                    return JsonResponse(None, status=404)
            else:
                return JsonResponse({'result': 'data filter not fount'}, status=500)
        else:
            return JsonResponse({'result': 'teacher not fount'}, status=500)


class CommentDataManageView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    paginator = pagination_class()

    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(status='published').order_by('-created_at')
        page = self.paginator.paginate_queryset(queryset, request)
        serializer = CommentWithAuthorSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            action = kwargs.get('action', False)
            if action == 'add':
                comment = Comment.objects.create(user_id=request.user.id, teacher_id=request.data.get('teacher_id'))
                serializer = CommentSerializer(comment, request.data, many=False, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return self.get(request=request, args=args, kwargs=kwargs)
                else:
                    return JsonResponse(serializer.errors)
        else:
            raise PermissionDenied()

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import *

User = get_user_model()


# teacher
class TeacherListSerializer(serializers.ModelSerializer):
    vote_rating = serializers.SerializerMethodField()
    vote_stars = serializers.SerializerMethodField()
    vote_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    specialization_name = serializers.SerializerMethodField()
    workplace_name = serializers.SerializerMethodField()

    def get_vote_rating(self, teacher):
        return teacher.vote.sum_rating()

    def get_vote_stars(self, teacher):
        return teacher.vote.get_stars()

    def get_vote_count(self, teacher):
        return teacher.vote.count()

    def get_comment_count(self, teacher):
        return teacher.comments.count()

    def get_specialization_name(self, teacher):
        return teacher.specialization.name

    def get_workplace_name(self, teacher):
        current = teacher.workplaces.filter(end_date=None).first()
        if current is None:
            current = teacher.workplaces.order_by('end_date').first()
        return current.name if current else ''

    class Meta:
        model = Teacher
        fields = (
            'id',
            'first_name',
            'last_name',
            'sur_name',
            'slug',
            'photo',
            'post',
            'workplace_name',
            'specialization_name',
            'vote_rating',
            'vote_stars',
            'vote_count',
            'comment_count'
        )


class TeacherDetailSerializer(TeacherListSerializer, serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    portfolios = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_username(self, teacher):
        return teacher.user.username

    def get_address(self, teacher):
        address = ''
        location = teacher.location
        if location:
            address = location.name
            district = location.district
            if district:
                address = f'{address}, {district.name}'
                region = district.region
                if region:
                    address = f'{address}, {region.name}'
        return address

    def get_portfolios(self, teacher):
        portfolios = {}
        for portfolio in teacher.portfolios.all():
            portfolios[portfolio.id] = {
                'title': portfolio.title,
                'image': portfolio.image.url
            }
        return portfolios

    def get_user_id(self, teacher):
        return teacher.user.id

    class Meta:
        model = Teacher
        fields = (
            'id',
            'user_id',
            'location_id',
            'specialization_id',
            'status',
            'username',
            'first_name',
            'last_name',
            'sur_name',
            'slug',
            'photo',
            'post',
            'birth_date',
            'gender',
            'workplace_name',
            'specialization_name',
            'address',
            'about',
            'portfolios',
            'vote_rating',
            'vote_stars',
            'vote_count',
            'comment_count'
        )


class TeacherEditCareerSerializer(TeacherListSerializer, serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = (
            'id',
            'specialization_name',
            'post',
            'portfolios',
            'workplaces'
        )


# teacher data

class TeacherSerializer(serializers.ModelSerializer):
    location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())

    class Meta:
        model = Teacher
        fields = (
            'id',
            'first_name',
            'last_name',
            'sur_name',
            'birth_date',
            'gender',
            'is_repetiteur',
            'price_per_hour',
            'photo',
            'post',
            'about',
            'location_id'
        )


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'name', 'district_id')


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ('id', 'name', 'region_id')


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('id', 'name')


class PortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = ('id', 'title', 'image', 'link', 'file')


class WorkplaceSerializer(serializers.ModelSerializer):
    teacher_id = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())

    class Meta:
        model = Workplace
        fields = ('id', 'name', 'post', 'start_date', 'end_date', 'teacher_id')


class TeacherAccountSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_user_type(self, obj):
        return obj.user.user_type

    class Meta:
        model = Teacher
        fields = ['id', 'username', 'email', 'user_type', 'first_name', 'last_name', 'sur_name']


class TeacherManageSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'sur_name', 'email', 'password', 'password2')

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).count() > 1:
            raise serializers.ValidationError({'email': 'Bunday email bazada mavjud!'})
        return attrs

    def update(self, instance, validated_data):
        email = validated_data.get('email')
        if instance.user.email != email:
            instance.user.email = email
            instance.user.save()
        return super().update(instance, validated_data)


class TeacherRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    sur_name = serializers.CharField(max_length=30, required=False)

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'sur_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        user.teacher.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            sur_name=validated_data.get('sur_name'),
        )

        return user


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'user_id', 'teacher_id', 'text', 'reply', 'status', 'updated_at')
        read_only_fields = ('created_at',)


class CommentWithAuthorSerializer(serializers.ModelSerializer):
    author_id = serializers.SerializerMethodField()
    author_slug = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    def get_author_id(self, obj):
        teacher = Teacher.objects.filter(user__id=obj.user_id).first()
        if teacher:
            return teacher.id
        else:
            return 0

    def get_author_slug(self, obj):
        teacher = Teacher.objects.filter(user__id=obj.user_id).first()
        if teacher:
            return teacher.slug
        else:
            return ''

    def get_full_name(self, obj):
        teacher = Teacher.objects.filter(user__id=obj.user_id).first()
        if teacher:
            result = f'{teacher.first_name} {teacher.last_name} {teacher.sur_name}'
        return result

    def get_photo(self, obj):
        teacher = Teacher.objects.filter(user__id=obj.user_id).first()
        if teacher and teacher.photo:
            return teacher.photo.url
        else:
            return ''

    class Meta:
        model = Comment
        fields = ('id', 'author_id', 'author_slug', 'full_name', 'photo', 'text')
        read_only_fields = ('updated_at',)

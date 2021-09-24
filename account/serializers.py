from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.utils.text import slugify

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'user_type')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'groups']


class UserManageSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs.get('password') and attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def update(self, instance, validated_data):
        if instance.email != validated_data.get('email'):
            instance.email = validated_data.get('email', instance.email)

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if validated_data.get('password'):
            instance.set_password(validated_data['password'])

        return super().update(instance, validated_data)


class AccountRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    sur_name = serializers.CharField(write_only=True, required=False)
    training_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'user_type',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
            'sur_name',
            'training_name'
        )

        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'sur_name': {'required': False},
            'training_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user_type = validated_data.get('user_type')
        account = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            user_type=user_type,
            is_superuser=False,
            is_staff=False
        )

        account.set_password(validated_data['password'])
        account.save()

        if user_type == 'user':
            account.user.create(
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name')
            )

        elif user_type == 'teacher':
            teacher = account.teacher.create(
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                sur_name=validated_data.get('sur_name')
            )
            slug_str = '%s %s %s %s' % (teacher.id, teacher.first_name, teacher.last_name, teacher.sur_name)
            teacher.slug = slugify(slug_str)
            teacher.save()

        elif user_type == 'training':
            training = account.trainings.create(name=validated_data.get('training_name'))
            slug_str = '%s %s' % (training.id, training.name)
            training.slug = slugify(slug_str)
            training.save()

        return account

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import *


class UserAccountSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    password = serializers.CharField(write_only=True, max_length=128, required=False, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, max_length=128, required=False)

    class Meta:
        model = UserAccount
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'photo', 'password', 'password2')
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'password': {'required': False},
            'password2': {'required': False}
        }

    def validate(self, attrs):
        if attrs.get('password') and attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def update(self, instance, validate_data):
        if validate_data.get('password'):
            instance.user.set_password(validate_data.get('password'))
            instance.user.save()
        return super().update(instance=instance, validated_data=validate_data)

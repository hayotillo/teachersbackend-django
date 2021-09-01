from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


# user
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


# teacher
class TeacherSerializers(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name', 'sur_name')



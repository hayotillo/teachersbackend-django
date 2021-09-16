from rest_framework import serializers
from django.contrib.auth.models import User


# user
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'last_login', 'is_active')


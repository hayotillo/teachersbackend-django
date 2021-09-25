from django.utils.text import slugify
from rest_framework import serializers
from .models import *
from teachers.models import Teacher
from training.models import Training


class CourseSerializer(serializers.ModelSerializer):

    model_name = serializers.CharField(write_only=True, max_length=20)

    class Meta:
        model = Course
        fields = ('id', 'name', 'slug', 'start_time', 'object_id', 'model_name')
        extra_kwargs = {
            'model_name': {'required': True}
        }

    def validate(self, attrs):
        return attrs

    def create(self, validate_data):
        object_id = validate_data.get('object_id')
        model_name = validate_data.get('model_name')
        if model_name == 'teacher':
            model = Teacher.objects.filter(pk=object_id).first()
        elif model_name == 'training':
            model = Training.objects.filter(pk=object_id).first()

        if model:
            del validate_data['model_name']
            content_type = ContentType.objects.get_for_model(model)

            validate_data['content_type_id'] = content_type.id
            validate_data['slug'] = slugify(f"{validate_data.get('name')} {validate_data.get('start_time')}")
            instance = super().create(validated_data=validate_data)

            return instance
        else:
            return None



from rest_framework import serializers
from .models import *


class BookDetailSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()

    def get_file_url(self, obj):
        return obj.url if obj.url else obj.file.url

    def get_subject_name(self, obj):
        return obj.subject.name

    class Meta:
        model = Book
        fields = ('id', 'name', 'file_url', 'subject_name')


class BookListSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()
    grade_number = serializers.SerializerMethodField()
    publisher_name = serializers.SerializerMethodField()
    author_names = serializers.SerializerMethodField()

    def get_subject_name(self, obj):
        return obj.subject.name

    def get_grade_number(self, obj):
        return obj.subject.grade.number if obj.subject.grade else ''

    def get_publisher_name(self, obj):
        return obj.publisher.name if obj.publisher else ''

    def get_author_names(self, obj):
        names = ''
        first = True
        for name in obj.authors.all():
            names = f'{names}{"" if first else ", "}{name}'
            first = False
        return names

    class Meta:
        model = Book
        fields = ('id',
                  'name',
                  'slug',
                  'image',
                  'subject_name',
                  'grade_number',
                  'publisher_name',
                  'year',
                  'author_names',
                  'format',
                  'pages',
                  'quality'
                  )

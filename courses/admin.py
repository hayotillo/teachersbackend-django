from django.contrib import admin
from .models import *


class CourseAdmin(admin.ModelAdmin):

    fields = ('name', 'start_time', 'end_time', 'description', 'price', 'content_type')
    readonly_fields = ('content_type',)


admin.site.register(Course, CourseAdmin)

from django.contrib import admin
from .models import *


# teacher
class TeacherAdmin(admin.ModelAdmin):
    fields = (
        'photo_tag',
        'photo',
        'first_name',
        'last_name',
        'sur_name',
        'status',
        'about',
        'phone',
        'phone2',
        'post',
        'telegram',
        'youtube',
        'email',
        'location',
        'specialization'
    )
    readonly_fields = ('photo_tag',)


# region
class RegionAdmin(admin.ModelAdmin):
    fields = ('name',)


# district
class DistrictAdmin(admin.ModelAdmin):
    fields = ('name', 'region')


# location
class LocationAdmin(admin.ModelAdmin):
    fields = ('name', 'district')


# specialization
class SpecializationAdmin(admin.ModelAdmin):
    fields = ('name',)


# workplace
class WorkplaceAdmin(admin.ModelAdmin):
    fields = ('name', 'teacher')


# comment
class CommentAdmin(admin.ModelAdmin):
    fields = ('name',)


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Workplace, WorkplaceAdmin)
admin.site.register(Comment, CommentAdmin)

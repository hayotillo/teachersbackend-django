from django.contrib import admin
from .models import *


# teacher
class TeacherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('first_name', 'last_name', 'sur_name')}
    fields = (
        'username_tag',
        'photo_tag',
        'photo',
        'first_name',
        'last_name',
        'sur_name',
        'slug',
        'status',
        'about',
        'birth_date',
        'gender',
        'phone',
        'phone2',
        'post',
        'telegram',
        'youtube',
        'location',
        'specialization'
    )
    readonly_fields = ('username_tag', 'photo_tag')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()


# portfolio
class PortfolioAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)
    fields = ('image_tag', 'title', 'image', 'link', 'file', 'teacher')


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
    fields = ('name', 'start_date', 'end_date', 'teacher')


# comment
class CommentAdmin(admin.ModelAdmin):
    fields = ('user', 'teacher', 'status', 'text')


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Workplace, WorkplaceAdmin)
admin.site.register(Comment, CommentAdmin)

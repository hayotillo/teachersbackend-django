from django.contrib import admin
from django.utils.text import slugify
from .models import *


class GradeAdmin(admin.ModelAdmin):

    fields = ('number',)


class SubjectAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'grade')
    readonly_fields = ('id',)


class PublisherAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug')


class AuthorAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('full_name',)}
    fields = ('full_name', 'slug')


class BookAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('subject', 'name')}
    readonly_fields = ('image_tag', 'created_at', 'updated_at')
    fields = ('image_tag',
              'image',
              'file',
              'url',
              'name',
              'slug',
              'status',
              'subject',
              'publisher',
              'year',
              'format',
              'pages',
              'quality',
              'authors'
              )

    def save_model(self, request, obj, form, change):
        is_new = not change
        if is_new:
            obj.user = request.user
        obj.save()

        obj.slug = slugify(f'{obj.id} {obj.subject} {obj.name}')
        obj.save()


admin.site.register(Grade, GradeAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)

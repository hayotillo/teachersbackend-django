from django.urls import path, include, re_path
from django.conf.urls import url
from rest_framework import routers
from rest_framework.authtoken import views
from django.contrib.auth.decorators import login_required
from .views import *
from .models import *

urlpatterns = [
    url(r'auth/', views.obtain_auth_token),
    # teacher vote
    url(
        r'vote-teacher/(?P<pk>\d+)/(?P<like_type>like|dislike)/',
        view=VoteView.as_view({'get': 'like'}),
        kwargs={'model': Teacher}
    ),
    url(r'list/(?P<page>\d+)/$', view=TeacherView.as_view({'get': 'list'}))
]

from django.urls import path, include, re_path
from django.conf.urls import url
from rest_framework import routers

from django.contrib.auth.decorators import login_required
from .views import *
from .models import *

urlpatterns = [
    # auth
    url(r'auth/', view=TeacherObtainAuthToken.as_view()),
    # logout
    url(r'logout/', Logout.as_view()),
    # create teacher account
    url(r'register/', view=Register.as_view()),
    url(r'manage-account/', view=ManageTeacherAccount.as_view()),
    # teacher vote
    url(
        r'vote-teacher/(?P<pk>\d+)/(?P<like_type>like|dislike)/',
        view=VoteView.as_view({'get': 'like'}),
        kwargs={'model': Teacher}
    ),
    url(r'check-token', view=TeacherView.as_view({'get': 'check_token'})),
    url(
        r'save/(?P<data_type>main|location|portfolio|workplace|account)',
        view=ManageDataView.as_view({'post': 'save'})
    ),
    url(
        r'delete/(?P<data_type>portfolio|workplace)/(?P<pk>\d+)',
        view=ManageDataView.as_view({'post': 'delete'})
    ),
    url(
        r'data/(?P<data_filter>short|main|location|portfolio|workplace|account)',
        view=DataView.as_view()
    ),
    url(r'short-data', view=ShortData.as_view()),
    url(r'detail/(?P<pk>\d+|me)', view=TeacherView.as_view({'get': 'teacher'})),
    url(r'list', view=TeacherListView.as_view())
]

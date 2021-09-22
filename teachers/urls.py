from django.urls import path, include, re_path
from django.conf.urls import url
from rest_framework import routers

from django.contrib.auth.decorators import login_required
from .views import *
from .models import *

urlpatterns = [
    # # teacher vote
    # url(
    #     r'vote-teacher/(?P<pk>\d+)/(?P<like_type>like|dislike)/',
    #     view=VoteView.as_view({'post': 'like'}),
    #     kwargs={'model': Teacher}
    # ),
    # # comment
    # url(
    #     r'comment/(?P<teacher_id>\d+)/(?P<action>list|add|remove)',
    #     view=CommentDataManageView.as_view()
    # ),
    # # check token
    # url(r'check-token', view=TeacherView.as_view({'get': 'check_token'})),
    # # manage portfolio
    # url(
    #     r'save/(?P<data_type>main|location|portfolio|workplace|account)',
    #     view=ManageDataView.as_view({'post': 'save'})
    # ),
    # # delete portfolio or workplace
    # url(
    #     r'delete/(?P<data_type>portfolio|workplace)/(?P<pk>\d+)',
    #     view=ManageDataView.as_view({'post': 'delete'})
    # ),
    # # cabinet data
    # url(
    #     r'data/(?P<data_filter>short|main|location|portfolio|workplace|account)',
    #     view=DataView.as_view()
    # ),
    # # detail teacher
    # url(r'detail/(?P<pk>\d+|me)', view=TeacherView.as_view({'get': 'teacher'})),
    # # teacher list by paginate
    # url(r'list', view=TeacherListView.as_view())
]

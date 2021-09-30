from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    path('list/', ListView.as_view()),
    url(r'detail/(?P<pk>\d+)', view=DetailView.as_view({'get': 'get_detail'}))
]

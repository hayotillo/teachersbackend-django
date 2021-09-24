from django.conf.urls import url
from django.urls import path, include
from .views import *


urlpatterns = [
    url('data/(?P<data_type>main)', view=DataView.as_view({'get': 'get_data'})),
    path('save/', SaveView.as_view()),
]

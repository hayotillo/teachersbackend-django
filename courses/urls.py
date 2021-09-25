from django.urls import path
from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'list/(?P<object_id>\d+)/', view=ListView.as_view()),
    url(r'save/', view=DataManageView.as_view({'post': 'save'})),
    url(r'delete/', view=DataManageView.as_view({'post': 'delete'})),
    url(r'detail/(?P<object_id>\d+)/', view=DetailView.as_view({'get': 'get_detail'})),
]

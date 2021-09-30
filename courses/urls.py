from django.urls import path
from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'list-all/', view=ListAllView.as_view()),
    url(
        r'list/(?P<model_name>teacher|training)/(?P<object_id>\d+|fcu)',
        view=ListView.as_view()
    ),
    url(r'save/', view=DataManageView.as_view({'post': 'save'})),
    url(
        r'delete/(?P<model_name>teacher|training)/(?P<pk>\d+)/',
        view=DataManageView.as_view({'post': 'delete'})
    ),
    url(r'detail/(?P<pk>\d+)/', view=DetailView.as_view({'get': 'get_detail'})),
]

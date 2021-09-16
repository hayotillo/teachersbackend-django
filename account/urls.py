from django.conf.urls import url
from rest_framework.authtoken import views
from .views import *

urlpatterns = [
    url(r'login/', views.obtain_auth_token),
    url(r'logout/', LogoutView.as_view()),
    url(r'get-user/(?P<pk>\d+|me)/$', UserView.as_view())
]

from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('register/', RegisterAccount.as_view()),
    path('login/', AuthTokenLogin.as_view()),
    path('logout/', Logout.as_view()),
    path('check-token/', CheckLogin.as_view()),
    # short info
    url(r'short-data/', view=ShortData.as_view()),
    url(r'data/main/', DataView.as_view()),
    path('update/', UpdateUser.as_view())
]

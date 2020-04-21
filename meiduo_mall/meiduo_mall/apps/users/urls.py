from django.conf.urls import re_path
from . import views
urlpatterns=[
    re_path(r'^register/$', views.RegisterView.as_view()),
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameView.as_view()),
    re_path(r'^mobiles/(?P<mobile>1[345789]\d{9})/count/$', views.MobileView.as_view()),
]
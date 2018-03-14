# -*-coding: utf-8-*-
from django.conf.urls import url
from class_interface.views import *


urlpatterns = [
    url(r'^index/$', index),
    url(r'^courses/(?P<pk>\d+)/tests/$', get_all_test),
    url(r'^tests/(?P<pk>\d+)/', get_current_test),
    url(r'^courses/$', get_all_course_info),
    url(r'^courses/(?P<pk>\d+)/$', get_current_course_data),
    url(r'^reverse_status/tests/(?P<pk>\d+)/$', reverse_the_status),
    url(r'^get_status/tests/(?P<pk>\d+)/$', get_the_status),
    url(r'^homework/$', post_homework),
]

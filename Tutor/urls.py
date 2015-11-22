from django.conf.urls import include, url
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^login/$',login),
    url(r'^logout/$',logout),
    url(r'^register/$',register),
    url(r'^index/$',index),
    url(r'^info/$',myinfo),
    url(r'^admin/',include(admin.site.urls)),
]   

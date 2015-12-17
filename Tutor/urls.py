from django.conf.urls import include, url
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^/$',mainpage),
    url(r'^login/$',login),
    url(r'^logout/$',logout),
    url(r'^register/$',register),
    url(r'^index/$',index),
    url(r'^info/$',myinfo),
    url(r'^upload/$',uploadimage),
    url(r'^search/$',search),
    url(r'^search_tutor/',searchTutor),
    url(r'^publishform/$',publishform),
    url(r'^admin/',include(admin.site.urls)),
    url(r'^message/(\d+)/$',message),
    url(r'^comment/(\d+)/$',comment),
    url(r'^employform/(\d+)/$',showdetail),
    url(r'^share/$',share),
    url(r'^information/p/(\d+)/$',pinformation),
    url(r'^information/t/(\d+)/$',tinformation),
]   

from django.conf.urls import include, url
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^$',mainpage),
    url(r'^login/$',login),
    url(r'^logout/$',logout),
    url(r'^register/$',register),
    url(r'^index/$',index),
    url(r'^info/$',myinfo),
    url(r'^upload/$',uploadimage),
    url(r'^search/',search),
    url(r'^search_tutor/$',searchTutor),
    url(r'^publishform/$',publishform),
    url(r'^admin/',include(admin.site.urls)),
    url(r'^message/$',message),
    url(r'^comment/$',comment),
    url(r'^hire/$',hire),
    url(r'^askemploy/(\d+)/$',showaskemploy),
    url(r'^employ/(\d+)/$',showemploy),
    url(r'^share/$',share),
    url(r'^information/(\d+)/$',information),
    url(r'^forgetpassword/$',forgetPassword),
    url(r'^changepassword/$',changePassword),
    url(r'^activemail/(\d+)/(\w+)/$',activeMail),
    url(r'^setpassword/(\d+)/(\w+)/$',resetPassword),
    url(r'^exp/$',exp),
]   

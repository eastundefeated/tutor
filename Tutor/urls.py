from django.conf.urls import include, url
from django.contrib import admin
from Tutor.views import *

urlpatterns = [
    #url(r'^index/$',index),
    url(r'^login/$',login),
    url(r'^logout/$',logout),
    url(r'^register/$',register),
    url(r'^index_parent/$',index_parent),
    url(r'^myinfo_parent/$',myinfo_parent),
    url(r'^search_tutor/$',search_tutor),
    url(r'^employ_tutor/$',employ_tutor),
    url(r'^message_parent/$',message_parent),
    url(r'^comment_parent/$',comment_parent),

    url(r'^index_tutor/$',index_tutor),
    url(r'^message_tutor/$',message_tutor),
    url(r'^comment_tutor/$',comment_tutor),
    url(r'^myinfo_tutor/$',myinfo_tutor),


    url(r'^tutor/(.+)/$',tutor),
    url(r'^parent/(.+)/$',parent),
]   

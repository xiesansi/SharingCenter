"""shafil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from shafil.sharefile.views import  RegisterView,user_activate,login,logout,index
from shafil.sharefile.views import  files_center,user_center,test,upload_file

urlpatterns = [
    url(r'^$',index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registe/',  RegisterView.as_view(), name='register'),
    url('^login/',login),
    url('^logout/',logout),
    url(r'^account_activate/(?P<activation_key>\w+)/$', user_activate),
    url(r'^files_center/', files_center),
    url(r'^test/',test),
    url(r'^upload_files',upload_file),
]

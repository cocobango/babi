"""wage_reports URL Configuration

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
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^logout/$', 'reports.views.logout', name='main_logout'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', auth_views.login , name='main_login'),
    url(r'^accounts/profile/$', 'reports.views.index'), 
    url(r'^accounts/login/$', 'reports.views.redirect_to_real_login'),
    url(r'^my_login/', include('my_login.urls' , namespace='my_login')),
    url(r'^reports/', include('reports.urls' , namespace='reports') ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^my_test/', 'reports.views.my_test'),
]

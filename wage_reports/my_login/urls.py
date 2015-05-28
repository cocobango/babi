from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^messages/(?P<message_text>[\sa-zA-Z]+)$', views.messages, name='messages'),
    url(r'^register/$', views.register, name='register'),
]
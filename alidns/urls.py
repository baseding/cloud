from django.conf.urls import url
from . import views

app_name='alidns'
urlpatterns = [
    # ex: /alidns/
    url(r'^$', views.index, name='index'),
    url(r'^records/$', views.records, name='records'),
    url(r'^add/$', views.add, name='add'),
    url(r'^thanks/$', views.thanks, name='thanks'),
]


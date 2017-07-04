from django.conf.urls import url
from . import views

app_name='pings'
urlpatterns = [
    # ex: /pings/
    url(r'^$', views.index, name='index'),

]


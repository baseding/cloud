from django.conf.urls import url
from . import views

app_name='httpd'
urlpatterns = [
    # ex: /httpd/
    url(r'^$', views.index, name='index'),

]


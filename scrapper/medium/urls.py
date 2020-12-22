from django.conf.urls import url
from . import views

app_name = 'medium'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name = 'search'),
    url(r'^other_page/$', views.other_page, name = 'other_page'),
]
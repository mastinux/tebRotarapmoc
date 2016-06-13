from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^2$', views.index_2, name='index_2'),
    url(r'^3$', views.index_3, name='index_3'),
]
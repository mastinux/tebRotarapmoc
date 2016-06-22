from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='public_page'),
    url(r'^2$', views.index_2, name='refreshed_page'),
    url(r'^3$', views.index_3, name='listed_page'),
]

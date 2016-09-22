from django.conf.urls import include, url
from django.contrib import admin
from visualizer import url as visualizer_urls
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^visualizer/', include(visualizer_urls))
]

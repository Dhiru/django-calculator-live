from django.conf.urls import url
from django.contrib import admin
from logs.views import index, calculator


urlpatterns = [
    url(r'^$', index),
    url(r'^calculator/(?P<slug>[^/]+)/$', calculator),
    url(r'^admin/', admin.site.urls),
]

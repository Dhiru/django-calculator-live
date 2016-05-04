from django.conf.urls import url
from django.contrib import admin
from logs.views import index, calculator, log


urlpatterns = [
    url(r'^$', index),
    url(r'^calculator/(?P<slug>[^/]+)/$', calculator),
    url(r'^log/(?P<calculator_slug>[^/]+)/(?P<log_body>[^/]+)$', log),
    url(r'^admin/', admin.site.urls),
]

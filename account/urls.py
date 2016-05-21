from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^$', views.upload_file, name='upload_file'),
]
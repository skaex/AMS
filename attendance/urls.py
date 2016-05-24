from attendance import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.preview_excel, name='upload'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^login/$', auth_views.login, name="login"),
    url(r'^logout/$', auth_views.logout, name="logout"),
]

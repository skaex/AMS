from attendance import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.preview_excel, name='upload'),
]

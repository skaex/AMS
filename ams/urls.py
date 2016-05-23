from django.conf.urls import include, url
from django.contrib import admin

from .views import home

urlpatterns = [
    # Examples:
    # url(r'^$', 'ams.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home, name='home'),
    url(r'^attendance/', include('attendance.urls', namespace='attendance')),
    url(r'^account/', include('account.urls', namespace='account')),
]

from django.conf.urls import url, include
from django.contrib import admin
from archive import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^$', views.index, name="index"),
    url('^save/$', views.save, name="save"),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url('', include('social_django.urls', namespace='social'))
]

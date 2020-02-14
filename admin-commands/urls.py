"""URLs for the django-admin-commands app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.AdminCommandsInterfaceView.as_view(),
        name='admin_commands'),
)
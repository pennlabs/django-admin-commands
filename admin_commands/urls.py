"""URLs for the django-admin-commands app."""
from django.conf.urls import url

from . import views

app_name = "admin-commands"

urlpatterns = [
    url('', views.AdminCommandsInterfaceView.as_view(),
        name='admin_commands'),
]

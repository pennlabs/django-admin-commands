from django.urls import include, path


urlpatterns = [path("", include("django-admin-commands.urls", namespace="admin-commands"))]

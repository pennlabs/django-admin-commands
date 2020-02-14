from django.urls import include, path


urlpatterns = [path("", include("project-name.urls", namespace="project-name"))]

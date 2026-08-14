from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="dashboard"),
    path("host/", views.host, name="host"),
]
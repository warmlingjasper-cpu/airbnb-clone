from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("create/", views.house_create, name="house_create"),

    path("<int:pk>/", views.house_detail, name="house_detail"),

    path("<int:pk>/edit/", views.house_update, name="house_update"),
]
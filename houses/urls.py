from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("create/", views.house_create, name="house_create"),

    path("<int:pk>/", views.house_detail, name="house_detail"),

    path("<int:pk>/edit/", views.house_update, name="house_update"),

    path("<int:pk>/reserve/", views.house_reserve, name="house_reserve"),

    path("my-reservations/", views.my_reservations, name="my_reservations"),

    path("host-reservations/",views.host_reservations,name="host_reservations"),

    path("house-image/<int:pk>/delete/", views.house_image_delete,name="house_image_delete"),

]
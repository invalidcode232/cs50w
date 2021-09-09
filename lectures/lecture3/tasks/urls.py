from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="Index"),
    path("add", views.add, name="Add"),
]

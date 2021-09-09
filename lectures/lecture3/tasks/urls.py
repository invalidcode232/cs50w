from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path("", views.index, name="Index"),
    path("add", views.add, name="Add"),
]

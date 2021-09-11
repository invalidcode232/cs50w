from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new_entry, name="new"),
    path("edit", views.edit, name="edit"),
    path("random", views.random_entry, name="random"),
    path("<str:name>", views.wiki, name="wiki")
]

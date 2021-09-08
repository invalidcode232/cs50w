from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Index"),
    path("<str:name>", views.greet, name="greet"),
    path("hermione", views.hermione, name="hermione"),
]

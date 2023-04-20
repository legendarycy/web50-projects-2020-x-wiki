from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.load_results, name="search"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("edit_entry", views.new_entry, name="edit_entry"),
    path("random", views.random_page, name="random")
]

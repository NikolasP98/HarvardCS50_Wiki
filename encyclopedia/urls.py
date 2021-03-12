from django.urls import path

from . import views

app_name = 'wiki'

urlpatterns = [
	path("", views.index, name="index"),
	path("404", views.error404, name="page404"),
	path("wiki/<str:name>", views.wikiLink, name="article"),
	path("random", views.randomPage, name="random"),
	path("edit/<str:title>", views.editor, name="edit"),
	path("createpage", views.create, name="create"),
	path("delete/<str:title>", views.delete, name="delete"),
	# All good above this line!
	path("search/", views.search, name="search")
]

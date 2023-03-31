from django.urls import path, include
from . import views
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView, PostComment, PostDisplay
)

urlpatterns = [
    path("post/new/", BlogCreateView.as_view(), name="post_new"), # new
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"), # new
    path("post/<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"), # new
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"), # new
    path("", BlogListView.as_view(), name="home"),
]

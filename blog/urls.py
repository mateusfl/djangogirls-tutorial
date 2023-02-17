from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("tags<str:tags>", views.PostListView.as_view(), name="post_list"),
    path("post/<str:slug>/", views.post_detail, name="post_detail"),
    path("post/<str:slug>/edit/", views.post_edit, name="post_edit"),
    path("posts/new/", views.post_new, name="post_new"),
]

from django.urls import path
from . import views


app_name = "posts"
urlpatterns = [
    path("comments/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment_update"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.PostUpdateView.as_view(), name="update"),
    path("comments/create/", views.CommentCreateView.as_view(), name="comment_create"),
    path("comments/<int:pk>/", views.CommentDetailView.as_view(), name="comment_detail"),
    path("comments/", views.CommentListView.as_view(), name="comment_list"),
    path("create/", views.PostCreateView.as_view(), name="create"),
    path("", views.PostListView.as_view(), name="list")
]

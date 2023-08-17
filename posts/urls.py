from django.urls import path

from .views import PostCreateView, PostDetailView, PostListView, PostUpdateView

app_name = "posts"
urlpatterns = [
    path("create/", PostCreateView.as_view(), name="create"),
    path("<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("", PostListView.as_view(), name="list"),
    path("<int:pk>/update/", PostUpdateView.as_view(), name="update")
]
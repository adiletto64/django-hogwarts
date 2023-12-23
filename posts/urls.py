from django.urls import path
from . import views


app_name = "posts"
urlpatterns = [
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.PostUpdateView.as_view(), name="update"),
    path("create/", views.PostCreateView.as_view(), name="create"),
    path("", views.PostListView.as_view(), name="list")
]

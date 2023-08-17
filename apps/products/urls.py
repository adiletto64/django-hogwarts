from django.urls import path
from . import views


app_name = "products"
urlpatterns = [
    path("categories/<int:pk>/update/", views.CategoryUpdateView.as_view(), name="category_update"),
    path("create/", views.ProductCreateView.as_view(), name="create"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="detail"),
    path("", views.ProductListView.as_view(), name="list"),
    path("<int:pk>/update/", views.ProductUpdateView.as_view(), name="update"),
    path("categories/create/", views.CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("categories/", views.CategoryListView.as_view(), name="category_list")
]

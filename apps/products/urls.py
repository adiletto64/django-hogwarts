from django.urls import path
from . import views
from .views import CategoryDetailView, ProductListView, ProductUpdateView

app_name = "products"
urlpatterns = [
    path("create/", views.ProductCreateView.as_view(), name="create"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="detail"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("", ProductListView.as_view(), name="list"),
    path("<int:pk>/update/", ProductUpdateView.as_view(), name="update")
]

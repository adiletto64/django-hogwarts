from django.urls import path

from .views import AddEqualSignView, ExampleCreateView, ExampleDetailView, ExampleListView


urlpatterns = [
    path("<int:pk>/add-equal-sign/", AddEqualSignView.as_view(), name="add_equal_sign"),
    path("create/", ExampleCreateView.as_view(), name="create"),
    path("<int:pk>/", ExampleDetailView.as_view(), name="detail"),
    path("", ExampleListView.as_view(), name="list")
]    
    
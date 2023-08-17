from .models import Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from .models import Product


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "products/product_detail.html"


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "products/product_list.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ["id", "name", "description", "cost", "category"]
    template_name = "products/product_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("products:detail", args=[self.object.id])


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = ["id", "name", "description", "cost", "category"]
    template_name = "products/product_update.html"

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse("products:detail", args=[self.get_object().id])


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = "category"
    template_name = "categories/category_detail.html"


class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "categories/category_list.html"


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ["id", "name"]
    template_name = "categories/category_create.html"
    success_url = "/"


class CategoryUpdateView(UserPassesTestMixin, UpdateView):
    model = Category
    fields = ["id", "name"]
    template_name = "categories/category_update.html"
    success_url = "/"

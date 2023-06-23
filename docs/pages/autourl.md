# Auto url paths setting

If you are bored writing path for an every single view
this is for you. Pass your views module to `auto_urls` function
and it will write every path for you.


## Step 1

import you view module (views.py) and pass to auto_urls function

```python
from . import views

from hogwarts.autourl import auto_urls

urlpatterns = []
urlpatterns += auto_urls(views, app_name="products")
```

## Step 2

There are certain rules and conventions. Write your views according
(CBV - class based view, FBV - function based view)

rules for CBVs:
- name should end with `view`
- django generic views like DetailView, ListView e.t.c will be excluded
rules for FBV:
- name should end with `view`
- must be snake case

### What paths are generated

1. both path url and name without suffix 'view'
2. path name -> snake_case view name
3. path url -> url params (if needed) + kebab-case path name
4. `<int:pk>/` will be added if view inherit `DetailView, UpdateView and DeleteView`
5. path url without `list` if view inherits `ListView`
6. path url without provided app_name (e.g. `auto_urls(views, app_name="products")`)

Look example bellow
```python
# views.py
from django.views.generic import DetailView, ListView, View, UpdateView

# lets take this views
class UnreadMessagesView(View):
    ...
class MessagesListView(ListView):
    ...
class ProductDetailView(DetailView):
    ...
class ProductsListView(ListView):
    ...
class ProductUpdateView(UpdateView):
    ...
class OrderConfirmView(UpdateView):
    ...

# urls.py
from . import views
from hogwarts.autourl import auto_urls

app_name = "products"
urlpatterns = auto_urls(views, app_name= "products")

# expression above will be evaluated to
urlpatterns = [
    path('unread-messages/', UnreadMessagesView.as_view(), name="unread_messages"),
    path("/", views.ProductsListView.as_view(), name="list"), # Look path rule 5 and 6
    path("<int:pk>/", views.ProductDetailView.as_view(), name="detail"), # as it inherits DetailView url param was set
    path("<int:pk>/update/", views.ProductUpdateView.as_view(), name="update"),
    path("<int:pk>/order-confirm/", views.OrderConfirmView.as_view(), name="order_confirm")
]
```


## Customization

Use auto_path decorator to change path generation
> auth_path(path_name: str, path_url: Optional[str], detail: bool = False)

You can provide path name and detail if url param (`<int:pk>`) needed.
Provide path_url for fully custom url

```python
from hogwarts.autourl import auto_path

@auto_path("push_over", detail=True)
class RandomName(View):
    ...

# above will make
# path("<int:pk>/push-over", RandomName.as_view(), name="push_over")

```



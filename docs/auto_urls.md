# Auto url paths resolver
`auto_urls` function to automatically set paths to urlpatterns

## Usage

import you view module (views.py) and pass to auto_urls function

```python
from hogwarts.magic_urls import auto_urls

from . import views


urlpatterns = []
urlpatterns += auto_urls(views, app_name="products")
```
::: info
Look at [conventions](/conventions) to see what views you should write
and what urls will be generated
:::


## Customization

Use auto_path decorator to change path generation
> auth_path(path_name: str, path_url: Optional[str], detail: bool = False)

You can provide path name and detail if url param (`<int:pk>`) needed.
Provide path_url for fully custom url

```python
from hogwarts.magic_urls import custom_path

@auto_path("push_over", detail=True)
class RandomName(View):
    ...

# above will make
# path("<int:pk>/push-over", RandomName.as_view(), name="push_over")

```



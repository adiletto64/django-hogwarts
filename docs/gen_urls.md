# Urlpatterns generator

command line utility to generation urls for views. 
But first you must know several conventions

## Command
``` 
python manage.py genurls <app name>
```

## What it generates
::: info
It automatically generates app_name or uses existing in urls.py to create 
[url namespace](https://docs.djangoproject.com/en/4.2/topics/http/urls/#reversing-namespaced-urls).
We recommend prefix your views with app_name to get cleaner urls and path names
:::

Here is the table of what will be generated for app posts, and it's views

| Views          | URL              | Path name |
| -------------- | ---------------- | --------- |
| PostListView   | /                | list      |
| PostCreateView | create/          | create    |
| PostDetailView | <int:pk>/        | detail    |
| PostDeleteView | <int:pk>/delete/ | delete    |
| PostUpdateView | <int:pk>/update/ | update    |
| SetReadView    | set-read/        | set_read  |
| send_view      | send/            | send      |


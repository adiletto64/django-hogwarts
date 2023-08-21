# Conventions


### What urls will be generated

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

1. if view contains one of this words: 'create', 'detail', 'delete', 'update', then <int:pk> will be set 
to URL

2. if view has two or more words (except 'view' suffix) in url it will be dashed version (kebab-case)
in path name underscore (snake_case). For example:
```python
class ConfirmMessageView:
    pass

# will be generated to    
path("confirm-message/", ConfirmMessageView.as_view(), name="confirm_message")
```
3. as_view() function will be automatically called for class-based-views
4. if view starts with app name (specified in urls.py. Look [url namespace](https://docs.djangoproject.com/en/4.2/topics/http/urls/#reversing-namespaced-urls).)
it will be removed from URL and path name, and if also has 'list' word URL will be empty
For example:
```python 
app_name = "posts"
urlpatterns = [
    path("", PostListView.as_view(), name="list")
    path("<int:pk>/detail/", PostDetailView.as_view(), name="detail")
    ...
]
```
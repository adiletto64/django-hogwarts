# Views generator

Basic CRUD class-based-views generator.
Run `genviews` with app name and model name

```shell
# command
python manage.py genviews app-name model

# example
python manage.py genviews posts Post
```

Arguments:
- `--smart-mode, -s` if set it adds `LoginRequiredMixin` to create view and if model has a field 
`user, author, owner or creator` it sets this from request in `form_valid` function and checks user on update view
- `--model-is-namespace, -nm` adds corresponding `reverse` function for success_url


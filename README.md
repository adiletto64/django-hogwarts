<h1 align="center">Django hogwarts 🧙‍♂️</h1>
<h4 align="center">Management commands to generate views, urls and templates!</h4>

Use CLI commands to generate:
- basic create, update, list, detail views
- urlpatterns from views with REST like path urls
- form, table, detail templates (Bootstrap and django-crispy-forms by default)

---

## Installation
```shell
# pip
pip install django-hogwarts

# poetry
poetry add --dev django-hogwarts
```

add `hogwarts` to your `INSTALLED_APPS`:
``` python
INSTALLED_APPS = [
    ...
    "hogwarts"
]
```

## Usage

### Generate urls.py

```
python manage.py genurls <your-app-name>
```

Arguments:
- `--force-app-name`, `fan` override app_name in urls.py 

### Generate views.py
```
python manage.py genviews <your-app-name> <model-name>
```
Arguments
- `smart-mode`, `-s` adds login required, sets user for CreateView and checks if client is owner of object in UpdateView
- `model-is-namespace`, `-mn` adds success_url with name model as [namespace](https://docs.djangoproject.com/en/4.2/topics/http/urls/#url-namespaces)

### Generate templates

**[django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms) and
[crispy-bootstrap5](https://github.com/django-crispy-forms/crispy-bootstrap5) packages are required**

``` 
python manage.py gentemplates <your-app-name>
```

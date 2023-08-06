# Installation

## Step 1
install via pip
```shell
pip install django-hogwarts

# via poetry
poetry add --dev django-hogwarts
```

## Step 2

add `hogwarts` to your `INSTALLED_APPS`
``` python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'hogwarts'
]
```

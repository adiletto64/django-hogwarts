from . import views
from .magic_urls.autourls import auto_urls

app_name = "example"
urlpatterns = auto_urls(views, "example")

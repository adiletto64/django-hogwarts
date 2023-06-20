from . import views
from .autourl import auto_urls

app_name = "example"
urlpatterns = auto_urls(views, "example")

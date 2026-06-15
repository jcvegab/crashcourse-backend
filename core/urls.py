from django.conf import settings

from core.api import api

app_name = "api-0.1.0"

_all_urls = api.urls[0]
_docs_names = {"openapi-json", "openapi-view"}

urlpatterns = [p for p in _all_urls if p.name not in _docs_names]

if settings.DEBUG:
    urlpatterns += [p for p in _all_urls if p.name in _docs_names]

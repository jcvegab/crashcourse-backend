from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from core.schema import schema


@csrf_exempt
def graphql_view(request, *args, **kwargs):
    return GraphQLView.as_view(
        schema=schema,
        graphql_ide="graphiql" if settings.DEBUG else None,
    )(request, *args, **kwargs)


urlpatterns = [
    # ----- Admin -----
    path("admin/", admin.site.urls),
    # ----- GraphQL -----
    path("graphql/", graphql_view),
    # ----- REST API -----
    path("", include("core.urls")),
]

if settings.DEBUG is False and not settings.IS_PROD:
    urlpatterns += staticfiles_urlpatterns()

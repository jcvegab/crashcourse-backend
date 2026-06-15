from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # ----- Admin -----
    path("admin/", admin.site.urls),
    # ----- GraphQL -----
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG))),
    # ----- REST API -----
    path("", include("core.urls")),
]

if settings.DEBUG is False and not settings.IS_PROD:
    urlpatterns += staticfiles_urlpatterns()
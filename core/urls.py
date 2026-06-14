from django.urls import path

from . import views

urlpatterns = [
    path("auth/login/", views.login, name="auth-login"),
    path("auth/refresh/", views.refresh, name="auth-refresh"),
]

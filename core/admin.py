from django.contrib import admin
from .models import Course, Category, Subcategory
# from django.apps import apps

# Register your models here.
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Subcategory)

# app = apps.get_app_config("graphql_auth")

# for model_name, model in app.models.items():
#     admin.site.register(model)

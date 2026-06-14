import graphene
from graphene_django.types import DjangoObjectType

from .models import Category, Course


class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        convert_choices_to_enum = False


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class Query(graphene.ObjectType):
    course = graphene.Field(CourseType, id=graphene.Int())
    courses = graphene.List(CourseType)
    category = graphene.Field(CategoryType, id=graphene.Int())
    categories = graphene.List(CategoryType)

    def resolve_course(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Course.objects.filter(pk=id).first()
        return None

    def resolve_courses(self, info, **kwargs):
        return Course.objects.all()

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()


schema = graphene.Schema(query=Query)

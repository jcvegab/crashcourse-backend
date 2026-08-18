from __future__ import annotations

import strawberry
import strawberry_django
from strawberry import auto

from .models import Category, Course


@strawberry_django.type(Course, name="CourseType")
class CourseType:
    id: auto
    name: auto
    real_price: auto
    price: auto
    discount: auto
    level: auto
    score: auto
    tutor_username: auto
    users: auto
    category: CategoryType | None
    subcategory: CategoryType | None


@strawberry_django.type(Category, name="CategoryType")
class CategoryType:
    id: auto
    name: auto
    parent: CategoryType | None
    category_set: list[CategoryType]
    courses: list[CourseType]
    subcourses: list[CourseType]


@strawberry.type
class Query:
    @strawberry.field
    def course(self, id: int | None = strawberry.UNSET) -> CourseType | None:
        if id is strawberry.UNSET or id is None:
            return None
        return Course.objects.filter(pk=id).first()

    @strawberry.field
    def courses(self) -> list[CourseType | None] | None:
        return Course.objects.all()

    @strawberry.field
    def category(self, id: int | None = strawberry.UNSET) -> CategoryType | None:
        if id is strawberry.UNSET or id is None:
            return None
        return Category.objects.filter(pk=id).first()

    @strawberry.field
    def categories(self) -> list[CategoryType | None] | None:
        return Category.objects.all()


schema = strawberry.Schema(query=Query)

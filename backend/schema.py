import graphene
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Course, Category, Subcategory


class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        convert_choices_to_enum = False


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class SubcategoryType(DjangoObjectType):
    class Meta:
        model = Subcategory


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    course = graphene.Field(CourseType, id=graphene.Int())
    courses = graphene.List(CourseType)
    categories = graphene.List(CategoryType)

    def resolve_course(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return Course.objects.get(pk=id)
        return None

    def resolve_courses(self, info, **kwargs):
        return Course.objects.all()

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()

    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

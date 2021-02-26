import graphene

# import graphql_jwt
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass
    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

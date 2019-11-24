import graphene
import erplicense.schema
import users.schema
import project.schema
import graphql_jwt


class Query(project.schema.Query,
            users.schema.Query,
            erplicense.schema.Query,
            graphene.ObjectType):
    pass


class Mutation(project.schema.Mutation,
               users.schema.Mutation,
               erplicense.schema.Mutation,
               graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

import graphene
class Query(graphene.ObjectType):
    name = graphene.String(default='hello world')


schema = graphene.Schema(query=Query)
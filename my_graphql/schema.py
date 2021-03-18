import graphene
from .schema_posts import PostsQuery
from .schema_comments import CommentQuery
from .schema_user import UserQuery, UserMutate

class Query(PostsQuery,CommentQuery,UserQuery, graphene.ObjectType):
    pass 

class Mutation(UserMutate, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)


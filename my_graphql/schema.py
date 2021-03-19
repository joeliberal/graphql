import graphene
from .schema_posts import PostsQuery, PostMutate
from .schema_comments import CommentQuery, CommentMutate
from .schema_user import UserQuery, UserMutate

class Query(PostsQuery,CommentQuery,UserQuery, graphene.ObjectType):
    pass 

class Mutation(UserMutate,PostMutate,CommentMutate, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)


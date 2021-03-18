import graphene
from posts.schema import PostsQuery
from comments.schema import CommentQuery

class Query(PostsQuery,CommentQuery, graphene.ObjectType):
    pass 

schema = graphene.Schema(query=Query)
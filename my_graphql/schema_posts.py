import graphene
from graphene_django.types import DjangoObjectType,ObjectType
from posts.models import Post
from django.contrib.auth.models import User


class PostsTyppe(DjangoObjectType):
    class Meta:
        model = Post

class PostsQuery(ObjectType):
    posts = graphene.List(PostsTyppe)
    post = graphene.Field(PostsTyppe, id=graphene.Int())
    postuser = graphene.List(PostsTyppe, name=graphene.String())

    def resolve_postuser(parent, info, **kwargs):
        name = kwargs.get('name')
        if name is not None:
            return Post.objects.filter(user__username=name)
        return None

    def resolve_posts(parent, info, **kwargs):
        return Post.objects.all() 

   
    def resolve_post(parent, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Post.objects.get(id=id)
        return None


import graphene
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType,ObjectType
from .models import Post

class UserType(DjangoObjectType):
    class Meta:
        model = User

class PostTyppe(DjangoObjectType):
    class Meta:
        model = Post

class PostsQuery(ObjectType):
    posts = graphene.List(PostTyppe)
    user = graphene.List(UserType)

    def resolve_posts(parent, info, **kwargs):
        return Post.objects.all() 

    def resolve_user(parent, info, **kwargs):
        return User.objects.all()
import graphene
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType,ObjectType
from .models import Post

class UserType(DjangoObjectType):
    class Meta:
        model = User

class PostsTyppe(DjangoObjectType):
    class Meta:
        model = Post

class PostsQuery(ObjectType):
    posts = graphene.List(PostsTyppe)
    users = graphene.List(UserType)
    post = graphene.Field(PostsTyppe, id=graphene.Int())
    user = graphene.Field(UserType, username=graphene.String())
    postuser = graphene.List(PostsTyppe, name=graphene.String())

    def resolve_postuser(parent, info, **kwargs):
        name = kwargs.get('name')
        if name is not None:
            return Post.objects.filter(user__username=name)
        return None

    def resolve_posts(parent, info, **kwargs):
        return Post.objects.all() 

    def resolve_users(parent, info, **kwargs):
        return User.objects.all()

    def resolve_post(parent, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Post.objects.get(id=id)
        return None

    def resolve_user(parent, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            return User.objects.get(username=username)
        return None

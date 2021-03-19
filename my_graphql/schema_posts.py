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


class PostInput(graphene.InputObjectType):
    user = graphene.Int()
    slug = graphene.String()
    title = graphene.String()
    draft = graphene.Boolean()


class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)
    
    ok = graphene.Boolean(default_value=False)
    post = graphene.Field(PostsTyppe)

    @staticmethod
    def mutate(parent, info, input=None):
        user_instance = User.objects.get(id=input.user)
        post_instance = Post.objects.create(user=user_instance,slug=input.slug, title=input.slug, draft=input.draft)
        return CreatePost(post = post_instance, ok=ok)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean(default=False)
    post = graphene.Field(PostsTyppe)

    def mutate(parent, info, id):
        post_instance = Post.objects.get(id=id)
        post_instance.delete()
        ok = True
        return DeletePost(post=post_instance, ok=ok)


class PostUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        input = PostInput()

    ok = graphene.Boolean(default=Flase)
    post = graphene.Field(PostsTyppe)

    def mutate(parent, info, id, input=None):
        post_instance = Post.objects.get(id=id)

        post_instance.slug  = inpiut.slug   if inpiut.slug id not None else post_instance.slug
        post_instance.title = inpiut.title   if inpiut.title id not None else post_instance.title
        post_instance.draft = inpiut.draft   if inpiut.draft id not None else post_instance.draft 

        ok = True
        return PostUpdate(post=post_instance, ok=ok)

class PostMutate(ObjectType):
    post_create = CreatePost.Field()
    post_delete = DeletePost.Field()
    post_update = PostUpdate.Field()
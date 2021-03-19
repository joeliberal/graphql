import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from comments.models import Comment
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class CommentQuery(ObjectType):
    comments = graphene.List(CommentType)
    comment = graphene.Field(CommentType, id=graphene.Int())

    def resolve_comment(parent, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Comment.objects.get(id=id)
        return None
        
    def resolve_comments(parent, info, **kwargs):
        return Comment.objects.all()


class CommentInput(graphene.InputObjectType):
    user = graphene.Int()
    content_type = graphene.Int()
    object_id = graphene.Int()
    parent = graphene.Int()
    content = graphene.String()


class CommentCreate(graphene.Mutation):
    class Arguments:
        input = CommentInput()

    ok = graphene.Boolean(default=False)
    comment = graphene.Field(CommentType)

    @staticmethod
    def mutate(parent, inf , input=None):
        user_instance = User.objects.get(id=input.user)
        conten_instance = ContentType.objects.get(id = input.content_type)
        parent_instance = Comment.objects.get(id = input.parent)
        
        comment_instance = Comment.objects.create(user = user_instance, content_type=conten_instance, parent=parent_instance, content = input.content)
        ok=True
        return CommentCreate(comment=comment_instance, ok = ok)


class CommentDelete(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    comment = graphene.Field(CommentType)
    ok = graphene.Boolean(default=False)

    def mutate(parent, info, id):
        comment_instance = Comment.objects.get(id = id)
        comment_instance.delete()
        ok = True

        return CommentDelete(comment=comment_instance, ok=ok)

class CommentUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        input = CommentInput()

    ok = graphene.Boolean(default = False)
    comment = graphene.Field(CommentType)

    def mutate(parent, info, id, input=None):
        comment_instance = Comment.objects.get(id=id)
        
        comment_instance.content_type = input.content_type  if  isnot None else comment_instance.content_type
        comment_instance.object_id    = input.object_id  if  isnot None else comment_instance.object_id
        comment_instance.parent       = input.parent  if  isnot None else comment_instance.parent
        comment_instance.content      = input.content  if  isnot None else comment_instance.content
        comment_instance.save()

        ok = True
        return CommentUpdate(comment=comment_instance, ok=ok)


class CommentMutate(graphene.ObjectType):
    create_commnet = CommentCreate.Field()
    delete_comment = CommentDelete.Field()
    comment_update = CommentUpdate.Field()
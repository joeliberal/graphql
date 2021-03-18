import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Comment

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class CommentQuery(ObjectType):
    comments = graphene.List(CommentType)

    def resolve_comments(parent, info, **kwargs):
        return Comment.objects.all()
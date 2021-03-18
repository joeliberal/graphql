import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Comment

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
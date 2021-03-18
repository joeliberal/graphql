import graphene
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType, ObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = User

class UserQuery(ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, name=graphene.String())

    def resolve_users(parent, info, **kwargs):
        return User.objects.all()

    def resolve_user(parent, info, **kwargs):
        name = kwargs.get('name')
        if name is not None:
            return User.objects.get(username=name)
        return None

class UserInput(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(parent, info, input=None):
        user_instance = User.objects.create(username = input.username, email = input.email, password=input.password)
        return CreateUser(user=user_instance)

class UserMutate(ObjectType):
    create_user = CreateUser.Field()
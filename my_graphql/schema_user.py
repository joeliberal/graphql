import graphene
import graphql_jwt
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


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)

    user = graphene.Field(UserType)
    ok = graphene.Boolean(default_value=True)

    def mutate(parent, info, id, input=None):
        user_instance = User.objects.get(id=id)
        user_instance.username = input.username if input.username is not None else user_instance.username
        user_instance.email = input.email if input.email is not None else user_instance.email
        user_instance.password = input.password if input.password is not None else user_instance.password
        user_instance.save()
        ok = True
        return UpdateUser(user=user_instance, ok=ok)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    user = graphene.Field(UserType)
    ok = graphene.Boolean(default_value=False)

    def mutate(parent, info, id):
        user_instance = User.objects.get(id=id)
        user_instance.delete()
        ok = True
        return DeleteUser(user=user_instance, ok=ok)

class UserMutate(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()    
    
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
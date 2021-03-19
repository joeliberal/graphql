import graphene

class CommentInput(graphene.InputObjectType):
    users = graphene.list(graphene.Int) 
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
        users_list=[]
        for user in input.users:
            user_instance = USer.objects.get(id=user)
            users_list.append(user_instance)

    comment_instance = Comment.objects.create(content_type=input.content_type,object_id=input.object_id,parent=input.parent, content=input.content)
    comment_instance.user.set(users_list)
    ok = True
    return CommentCreate(comment=comment_instance, ok=ok)
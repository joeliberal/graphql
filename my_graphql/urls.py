from django.urls import path
from graphene_django.views import GraphQLView

app_name='my_graphql'

urlpatterns = [
    path('', GraphQLView.as_view(graphiql=True)),
]
from flask_openapi3 import OpenAPI, Info
from flask import redirect

import strawberry
from strawberry.flask.views import GraphQLView

from graphql_api.schemas import Query, Mutation
from logger import logger

info = Info(title="Forum API", version="1.0.0")

api = OpenAPI(__name__, info=info)

schema = strawberry.Schema(query=Query, mutation=Mutation)

api.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)


@api.get("/")
def home():
    """Redireciona para a rota graphql fornecidas pela biblioteca strawberry
    para a documentação da API graphql e para o GraphQL Explorer"""
    logger.debug("Redireciona para api graphql.")
    return redirect("/graphql")

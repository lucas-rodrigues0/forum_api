import strawberry
from pydantic import typing
import uuid
from datetime import datetime, timedelta

from graphql_api.scalars import Article, Comment
from graphql_api.resolvers import (
    get_articles,
    get_article_by_id,
    get_article_by_user,
    get_articles_by_period,
    get_comments,
    get_comment_by_id,
    get_comments_by_user,
    get_comments_by_period,
)


@strawberry.type(
    description="Query para a leitura de artigos e comentários existentes no banco de dados."
)
class Query:

    @strawberry.field(description="Query para leitura de todos artigos.")
    def articles(self) -> typing.List[Article]:
        articles_data_list = get_articles()
        return articles_data_list

    @strawberry.field(description="Query para leitura de artigo pelo seu ID.")
    def article_by_id(self, article_id: uuid.UUID) -> Article:
        articles_data = get_article_by_id(article_id)
        return articles_data

    @strawberry.field(
        description="Query para leitura de todos artigos de um usuário específico."
    )
    def articles_by_user_id(self, user_id: str) -> typing.List[Article]:
        articles_data_list = get_article_by_user(user_id)
        return articles_data_list

    @strawberry.field(
        description="Query para leitura de todos artigos de um determinado período."
    )
    def articles_by_period(
        self, initial_date: str, end_date: str
    ) -> typing.List[Article]:
        datetime_format = "%d-%m-%Y"
        initial_datetime = datetime.strptime(initial_date, datetime_format)
        end_datetime = datetime.strptime(end_date, datetime_format) + timedelta(days=1)
        articles_data_list = get_articles_by_period(initial_datetime, end_datetime)
        return articles_data_list

    @strawberry.field(description="Query para leitura de todos comentários.")
    def comments(self) -> typing.List[Comment]:
        comment_data_list = get_comments()
        return comment_data_list

    @strawberry.field(description="Query para leitura de comentário pelo seu ID.")
    def comment_by_id(self, comment_id: uuid.UUID) -> Comment:
        comment_data = get_comment_by_id(comment_id)
        return comment_data

    @strawberry.field(
        description="Query para leitura de todos comentários de um usuário específico."
    )
    def comment_by_user_id(self, user_id: str) -> typing.List[Comment]:
        comments_data_list = get_comments_by_user(user_id)
        return comments_data_list

    @strawberry.field(
        description="Query para leitura de todos comentários de um determinado período."
    )
    def comments_by_period(
        self, initial_date: str, end_date: str
    ) -> typing.List[Comment]:
        datetime_format = "%d-%m-%Y"
        initial_datetime = datetime.strptime(initial_date, datetime_format)
        end_datetime = datetime.strptime(end_date, datetime_format) + timedelta(days=1)
        comments_data_list = get_comments_by_period(initial_datetime, end_datetime)
        return comments_data_list

import strawberry
from typing import Union, Optional
import uuid

from graphql_api.scalars import (
    AddArticle,
    UserInfoMissing,
    ArticleContentMissing,
    ArticleDeleted,
    AddComment,
    CommentDeleted,
    CommentContentMissing,
    CommentReplyNotAllowed,
    InvalidUser,
)
from graphql_api.resolvers import (
    add_article,
    delete_article,
    update_article,
    add_comment,
    delete_comment,
    update_comment,
)


@strawberry.type(
    description="Mutation para inserção, atualização e remoção de artigos e comentários."
)
class Mutation:

    @strawberry.mutation(
        description="Mutation para a inserção de artigo no banco de dados."
    )
    def add_article(
        self,
        user_id: str,
        user_email: str,
        user_nickname: str,
        title: str,
        content: str,
    ) -> Union[AddArticle, UserInfoMissing, ArticleContentMissing]:
        article_dict = {
            "user_id": user_id,
            "user_email": user_email,
            "user_nickname": user_nickname,
            "title": title,
            "content": content,
        }
        add_article_resp = add_article(article_dict)
        return add_article_resp

    @strawberry.mutation(
        description="Mutation para a remoção de artigo do banco de dados."
    )
    def remove_article(
        self, article_id: uuid.UUID, user_id: str
    ) -> Union[ArticleDeleted, InvalidUser]:
        delete_article_resp = delete_article(article_id, user_id)
        return delete_article_resp

    @strawberry.mutation(
        description="Mutation para a atualização de artigo no banco de dados."
    )
    def update_article(
        self,
        article_id: uuid.UUID,
        user_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
    ) -> Union[AddArticle, InvalidUser]:
        article_dict = {"article_id": article_id, "user_id": user_id}
        if title:
            article_dict["title"] = title

        if content:
            article_dict["content"] = content

        update_article_resp = update_article(article_dict)
        return update_article_resp

    @strawberry.mutation(
        description="Mutation para a inserção de comentário no banco de dados."
    )
    def add_comment(
        self,
        user_id: str,
        user_email: str,
        user_nickname: str,
        article_id: uuid.UUID,
        content: str,
        is_reply: Optional[bool] = False,
        comment_reply: Optional[uuid.UUID] = None,
    ) -> Union[
        AddComment, UserInfoMissing, CommentReplyNotAllowed, CommentContentMissing
    ]:
        comment_dict = {
            "user_id": user_id,
            "user_email": user_email,
            "user_nickname": user_nickname,
            "article_id": article_id,
            "content": content,
        }

        if is_reply:
            comment_dict["is_reply"] = is_reply
        if comment_reply:
            comment_dict["comment_reply"] = comment_reply

        add_comment_resp = add_comment(comment_dict)
        return add_comment_resp

    @strawberry.mutation(
        description="Mutation para a remoção de comentário do banco de dados."
    )
    def remove_comment(
        self, comment_id: uuid.UUID, user_id: str
    ) -> Union[CommentDeleted, InvalidUser]:
        delete_comment_resp = delete_comment(comment_id, user_id)
        return delete_comment_resp

    @strawberry.mutation(
        description="Mutation para a atualização de comentário no banco de dados."
    )
    def update_comment(
        self, comment_id: uuid.UUID, user_id: str, content: str
    ) -> Union[AddComment, CommentContentMissing, InvalidUser]:
        comment_dict = {
            "comment_id": comment_id,
            "user_id": user_id,
            "content": content,
        }

        update_comment_resp = update_comment(comment_dict)
        return update_comment_resp

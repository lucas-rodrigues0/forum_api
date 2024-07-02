import datetime
import strawberry
import uuid

from typing import TYPE_CHECKING, Annotated, List, Optional


if TYPE_CHECKING:
    from .comment_scalar import Comment


@strawberry.type(description="Artigo inserido no forum")
class Article:
    article_id: uuid.UUID
    user_id: str
    user_email: str
    user_nickname: str
    title: str
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    comments: Optional[List[Annotated["Comment", strawberry.lazy(".comment_scalar")]]]


@strawberry.type
class AddArticle:
    article_id: uuid.UUID
    user_id: str
    user_email: str
    user_nickname: str
    title: str
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@strawberry.type
class ArticleDeleted:
    message: str = "Article deleted"


@strawberry.type
class UserInfoMissing:
    message: str = "User info is missing"


@strawberry.type
class ArticleContentMissing:
    message: str = "Article title or content is missing"

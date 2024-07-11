import datetime
import strawberry
import uuid

from typing import TYPE_CHECKING, Annotated, List, Optional


if TYPE_CHECKING:
    from .comment_scalar import Comment


@strawberry.type(description="Representação de Artigo e seus comentários.")
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


@strawberry.type(description="Representação de Artigo inserido no banco de dados.")
class AddArticle:
    article_id: uuid.UUID
    user_id: str
    user_email: str
    user_nickname: str
    title: str
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@strawberry.type(description="Mensagem de confirmação para remoção de Artigo.")
class ArticleDeleted:
    message: str = "Article deleted"


@strawberry.type(description="Mensagem de erro para dados de usuário ausente.")
class UserInfoMissing:
    errors: str = "User info is missing"


@strawberry.type(description="Mensagem de erro para dados de artigo ausente.")
class ArticleContentMissing:
    errors: str = "Article title or content is missing"


@strawberry.type(
    description="Mensagem de erro para usuário não válido para a operação."
)
class InvalidUser:
    errors: str = "Invalid user. You can only modify your own post."

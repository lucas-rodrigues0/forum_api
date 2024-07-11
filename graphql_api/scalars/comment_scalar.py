import datetime
import strawberry
import uuid

from typing import TYPE_CHECKING, Annotated, Optional, List


if TYPE_CHECKING:
    from .article_scalar import Article


@strawberry.type(
    description="Representação de um Comentário, seus comentários resposta e o artigo que se relaciona."
)
class Comment:
    comment_id: uuid.UUID
    user_id: str
    user_email: str
    user_nickname: str
    content: str
    is_reply: bool
    comment_reply: Optional[uuid.UUID]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    article_id: uuid.UUID
    article: Optional[Annotated["Article", strawberry.lazy(".article_scalar")]]
    replies: Optional[List[Annotated["Comment", strawberry.lazy(".comment_scalar")]]]


@strawberry.type(description="Representação de Comentário inserido no banco de dados.")
class AddComment:
    comment_id: uuid.UUID
    user_id: str
    user_email: str
    user_nickname: str
    content: str
    article_id: uuid.UUID
    article: Optional[Annotated["Article", strawberry.lazy(".article_scalar")]]
    is_reply: Optional[bool]
    comment_reply: Optional[uuid.UUID]
    created_at: datetime.datetime
    updated_at: datetime.datetime


@strawberry.type(description="Mensagem de confirmação para remoção de Comentário.")
class CommentDeleted:
    message: str = "Comment deleted"


@strawberry.type(description="Mensagem de erro para dados de comentário ausente.")
class CommentContentMissing:
    errors: str = "Comment content is missing"


@strawberry.type(
    description="Mensagem de erro para comentário resposta a outro comentário que também é uma resposta."
)
class CommentReplyNotAllowed:
    errors: str = "Comment can not be replied to another reply"

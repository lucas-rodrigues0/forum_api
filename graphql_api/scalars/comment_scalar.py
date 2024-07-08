import datetime
import strawberry
import uuid

from typing import TYPE_CHECKING, Annotated, Optional, List


if TYPE_CHECKING:
    from .article_scalar import Article


@strawberry.type(description="Comentário a um artigo")
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


@strawberry.type
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


@strawberry.type
class CommentDeleted:
    message: str = "Comment deleted"


@strawberry.type
class CommentContentMissing:
    errors: str = "Comment content is missing"


@strawberry.type
class CommentReplyNotAllowed:
    errors: str = "Comment can not be replied to another reply"

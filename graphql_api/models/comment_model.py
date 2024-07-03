from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Union
import uuid

from graphql_api.models import Base


class Comment(Base):
    __tablename__ = "comment"

    comment_id = Column(
        "comment_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id = Column(String(80), nullable=False)
    user_email = Column(String(100), nullable=False)
    user_nickname = Column(String(80), nullable=False)
    content = Column(String(1500), nullable=False)
    is_reply = Column(Boolean, default=False)
    comment_reply = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    article_id = Column(
        UUID(as_uuid=True), ForeignKey("article.article_id"), nullable=False
    )

    def __init__(
        self,
        user_id: str,
        user_email: str,
        user_nickname: str,
        content: str,
        article_id,
        is_reply: Union[bool, None] = False,
        comment_reply=None,
    ):
        self.article_id = article_id
        self.user_id = user_id
        self.user_email = user_email
        self.user_nickname = user_nickname
        self.content = content
        if is_reply:
            self.is_reply = is_reply
        if comment_reply:
            self.comment_reply = comment_reply

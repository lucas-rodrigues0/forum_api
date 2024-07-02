from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from graphql_api.models import Base


class Article(Base):
    __tablename__ = "article"

    article_id = Column(
        "article_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id = Column(String(80), nullable=False)
    user_email = Column(String(100), nullable=False)
    user_nickname = Column(String(80), nullable=False)
    title = Column(String(80), nullable=False)
    content = Column(String(350), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def __init__(
        self,
        user_id: str,
        user_email: str,
        user_nickname: str,
        title: str,
        content: str,
    ):
        self.user_id = user_id
        self.user_email = user_email
        self.user_nickname = user_nickname
        self.title = title
        self.content = content

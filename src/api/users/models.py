import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from api.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name = Column(String(50), nullable=False)

    password = Column(String(100), nullable=False)

    scope = Column(String(255), nullable=False, default="products:read")

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
    )
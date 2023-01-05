from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKeyConstraint
    )
from sqlalchemy.sql import func

from .conn import Base


class Users(Base):
    """User Table"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_active = Column(Boolean, nullable=False, default=True)


class Tokens(Base):
    """Refresh Token Table"""
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String(512), nullable=False)

    __tableargs__ = (
        ForeignKeyConstraint((user_id,), (Users.id,))
    )

from __future__ import annotations

from typing import List
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Table, TEXT
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
from sqlalchemy.sql import func

#class Base(DeclarativeBase):
#    pass
Base = declarative_base()

user_chat_association = Table(
    "user_chats",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("chat_id", ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True)
)


class Chat(Base):
    __tablename__ = 'chats'

    id: Mapped[int] = mapped_column(primary_key=True)

    name = Column(String(255), nullable=False)
    description = Column(TEXT, nullable=True)
    is_private = Column(Boolean, nullable=False, default=True)
    chat_owner_id = Column(Integer, ForeignKey('users.id'), nullable=False) 

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    chat_owner: Mapped[User] = relationship(back_populates="own_chats")

    users: Mapped[List[User]] = relationship(
        secondary=user_chat_association, back_populates="chats"
    )

    def __repr__(self):
        return f"<Chat(name={self.name}, is_private={self.is_private})>"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    pw_hash = Column(String(255), nullable=False)
    description = Column(TEXT, nullable=True, default='')

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    own_chats: Mapped[List[Chat]] = relationship(back_populates="chat_owner")

    chats: Mapped[List[Chat]] = relationship(
        secondary=user_chat_association, back_populates="users"
    )

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


#class UserChat(Base):
#    __tablename__ = 'user_chats'
#
#    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
#    chat_id = Column(Integer, ForeignKey('chats.id'), primary_key=True)
#
#    user = relationship("User", back_populates="user_chats")
#    chat = relationship("Chat", back_populates="user_chats")
#
#    def __repr__(self):
#        return f"<UserChat(user_id={self.user_id}, chat_id={self.chat_id})>"
#    

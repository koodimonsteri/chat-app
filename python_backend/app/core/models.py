from __future__ import annotations
from enum import Enum as PYEnum
import uuid
from typing import List

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Table,
    TEXT,
    UUID,
    Enum as SQLEnum
)
from sqlalchemy.orm import relationship, Mapped, declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class FriendshipStatus(PYEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ChatBotType(PYEnum):
    ASSISTANT = 'assistant'
    CUSTOM = 'custom'
    DEFAULT = 'default'


user_chat_association = Table(
    "user_chats",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("chat_id", ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True)
)

# This table represents bidirectional friendships. 
# Each row connects two users and there is no implied directionality.
# Only one row is stored for each friendship pair.
friendship_association = Table(
    'friendships',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('created_at', DateTime, server_default=func.now(), nullable=False)
)


chat_bots_association = Table(
    "chat_bots_association",
    Base.metadata,
    Column("bot_id", ForeignKey("chatbots.id", ondelete="CASCADE"), primary_key=True),
    Column("chat_id", ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True)
)


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    name = Column(String(255), nullable=False)
    description = Column(TEXT, nullable=True)
    is_private = Column(Boolean, nullable=False, default=True)

    chat_owner_id = Column(Integer, ForeignKey('users.id'), nullable=False) 
    chat_owner: Mapped[User] = relationship(back_populates="own_chats")

    chat_bots: Mapped[List["ChatBot"]] = relationship(
        "ChatBot", secondary=chat_bots_association, back_populates="chats"
    )

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    users: Mapped[List[User]] = relationship(
        secondary=user_chat_association, back_populates="chats"
    )

    def __repr__(self):
        return f"<Chat(name={self.name}, is_private={self.is_private})>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    pw_hash = Column(String(255), nullable=False)
    description = Column(TEXT, default='', nullable=True)

    openai_token = Column(String(255), default='', nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    own_chats: Mapped[List[Chat]] = relationship(
        "Chat", back_populates="chat_owner", cascade="all, delete-orphan"
    )
    chats: Mapped[List[Chat]] = relationship(
        secondary=user_chat_association, back_populates="users"
    )

    friends: Mapped[List[User]] = relationship(
        "User",
        secondary=friendship_association,
        primaryjoin=id == friendship_association.c.user_id,
        secondaryjoin=id == friendship_association.c.friend_id,
        back_populates='friends'
    )

    sent_requests: Mapped[List[FriendRequest]] = relationship(
        "FriendRequest",
        foreign_keys="[FriendRequest.sender_id]",
        back_populates="sender"
    )

    received_requests: Mapped[List[FriendRequest]] = relationship(
        "FriendRequest",
        foreign_keys="[FriendRequest.receiver_id]",
        back_populates="receiver"
    )

    user_bots: Mapped[List[ChatBot]] = relationship("ChatBot", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


class ChatMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False) 
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sender_username = Column(String(255), nullable=False)

    content = Column(TEXT)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Message(chat_id={self.chat_id}, sender_id={self.sender_id}, content={self.content})>"


class FriendRequest(Base):
    __tablename__ = 'friend_requests'

    id = Column(Integer, primary_key=True)
    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    sender_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    status = Column(SQLEnum(FriendshipStatus), nullable=False, default=FriendshipStatus.PENDING)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_requests")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_requests")

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ChatBot(Base):
    __tablename__ = 'chatbots'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    type = Column(SQLEnum(ChatBotType), default=ChatBotType.DEFAULT, nullable=False)
    system_prompt = Column(TEXT, nullable=True)
    api_token = Column(String(255), default='', nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="user_bots")

    chats: Mapped[List[Chat]] = relationship(
        "Chat", secondary=chat_bots_association, back_populates="chat_bots"
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())



import logging
from typing import List

from starlette.exceptions import HTTPException
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.exceptions import ResourceNotFoundError, DatabaseError
from core.models import User, FriendRequest
from schemas.friend_request import FriendshipStatus
from schemas.general import PaginationParams

logger = logging.getLogger('uvicorn')


async def get_all_users(db: AsyncSession, pagination: PaginationParams):
    result = await db.execute(
        select(User)
        #.options(joinedload(User.chats))
        #.options(joinedload(User.friends))
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
    return result.scalars().all()


async def get_user_by_name(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)

    return result.scalars().one_or_none()


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)

    return result.scalars().one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)

    return result.scalars().one_or_none()


async def get_user_with_friends(db: AsyncSession, user_id: int):
    query = (
        select(User)
        .where(User.id == user_id)
        .options(joinedload(User.friends))
    )
    result = await db.execute(query)
    return result.unique().scalars().one_or_none()


async def create_user(db: AsyncSession, new_user: User):
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user


async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    
    if not user:
        raise ResourceNotFoundError("User not found")

    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()

    return user


################################################
#           Friend request stuff               #
################################################

logger = logging.getLogger('uvicorn')


async def get_friend_requests(db: AsyncSession, user_id: int) -> List[FriendRequest]:
    query = (
        select(FriendRequest)
        .join(User, (FriendRequest.sender_id == User.id) | (FriendRequest.receiver_id == User.id))
        .where(
            (FriendRequest.sender_id == user_id) | (FriendRequest.receiver_id == user_id),
            FriendRequest.status == FriendshipStatus.PENDING
        )
        .options(
            joinedload(FriendRequest.sender),
            joinedload(FriendRequest.receiver),
        )
    )
    result = await db.execute(query)
    logger.info('result: %s', result)
    friend_requests = result.unique().scalars().all()
    logger.info('user: %s', friend_requests)


    return friend_requests


async def create_friend_request(db: AsyncSession, sender_id: int, username: str):
    receiver = await get_user_by_name(db, username)

    if not receiver:
        raise HTTPException(status_code=404, detail="User not found")

    if sender_id == receiver.id:
        raise HTTPException(status_code=400, detail="You cannot send a friend request to yourself")

    existing_request = await db.execute(select(FriendRequest).filter(
        (FriendRequest.sender_id == sender_id) & 
        (FriendRequest.receiver_id == receiver.id)
    ))
    existing_request = existing_request.unique().scalars().one_or_none()

    if existing_request:# and existing_request.status == FriendshipStatus.PENDING:
        raise HTTPException(status_code=400, detail="Friend request already sent")

    new_request = FriendRequest(sender_id=sender_id, receiver_id=receiver.id)
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)

    return new_request


async def accept_friend_request(db: AsyncSession, user_id: int, request_id: int):
    friend_request = await db.execute(
        select(FriendRequest)
        .filter(FriendRequest.id == request_id)
        .options(joinedload(FriendRequest.sender), joinedload(FriendRequest.receiver))
    )
    friend_request = friend_request.unique().scalars().one_or_none()

    if not friend_request:
        raise HTTPException(status_code=404, detail="Friend request not found")
    
    if friend_request.receiver_id != user_id:
        raise HTTPException(status_code=400, detail="This friend request is not for you")
    
    if friend_request.status == FriendshipStatus.ACCEPTED:
        raise HTTPException(status_code=400, detail="Friend request already accepted")

    friend_request.status = FriendshipStatus.ACCEPTED
    db.add(friend_request)

    sender = await get_user_with_friends(db, friend_request.sender_id)
    receiver = await get_user_with_friends(db, friend_request.receiver_id)

    if sender and receiver:
        sender.friends.append(receiver)
        receiver.friends.append(sender)
    else:
        raise DatabaseError('Failed to create friendship :(')
    
    await db.commit()
    await db.refresh(friend_request)
    
    return friend_request


async def reject_friend_request(db: AsyncSession, user_id: int, request_id: int):
    friend_request = await db.execute(select(FriendRequest).filter(FriendRequest.id == request_id))
    friend_request = friend_request.unique().scalars().one_or_none()
    if not friend_request:
        raise HTTPException(status_code=404, detail="Friend request not found")
    logger.info('Found friend request: %s', friend_request)

    if friend_request.receiver_id != user_id:
        raise HTTPException(status_code=400, detail="This friend request is not for you")

    if friend_request.status == FriendshipStatus.REJECTED:
        raise HTTPException(status_code=400, detail="Friend request already rejected")

    friend_request.status = FriendshipStatus.REJECTED
    db.add(friend_request)

    await db.commit()
    await db.refresh(friend_request)
    logger.info('Refreshed: %s', friend_request)
    return friend_request
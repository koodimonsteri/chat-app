import os
import asyncio

from core.database import AsyncSessionLocal
from core.models import User, UserRole#, Base
#from passlib.context import CryptContext
#from core import settings
from routes.auth import pwd_context

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "adminpassword")

async def prefill_admin():
    async with AsyncSessionLocal() as session:
        async with session.begin():

            hashed_password = pwd_context.hash(ADMIN_PASSWORD)

            admin_user = User(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                pw_hash=hashed_password,
                role=UserRole.ADMIN
            )

            session.add(admin_user)
            await session.commit()

if __name__ == "__main__":
    asyncio.run(prefill_admin())

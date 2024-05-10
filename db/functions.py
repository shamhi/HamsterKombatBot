from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from db.models import Account, Crypto, Logs


async def get_user_agent(db_pool: async_sessionmaker, phone_number: int) -> str:
    async with db_pool() as db_session:
        query = select(Crypto.userAgent).where(Crypto.account__ID == phone_number)
        result = await db_session.execute(query)
        user_agent = result.scalars().one_or_none()

        return user_agent or ''


async def get_user_proxy(db_pool: async_sessionmaker, phone_number: int) -> str:
    async with db_pool() as db_session:
        query = select(Crypto.proxy).where(Crypto.account__ID == phone_number)
        result = await db_session.execute(query)
        proxy = result.scalars().one_or_none()

        return proxy


async def save_log(db_pool: async_sessionmaker, phone: int, status: str, amount: str) -> None:
    async with db_pool() as db_session:
        new_log = Logs(
            phone=phone,
            datetime=datetime.now(),
            botName="HamsterKombatBot",
            status=status,
            amount=amount,
        )

        db_session.add(new_log)
        await db_session.commit()

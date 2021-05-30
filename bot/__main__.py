import asyncio
import logging

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.db.base import Base
from bot.handlers.commands import register_commands
from bot.handlers.callbacks import register_callbacks


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    # TODO: move these values to env vars or some config file (also in docker-compose)
    engine = create_async_engine(
        "postgresql+asyncpg://demo:4hunger0shirt1what4@localhost/demo_db",
        future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    bot = Bot("TOKEN", parse_mode="HTML")
    bot["db"] = async_session
    dp = Dispatcher(bot)

    register_commands(dp)
    register_callbacks(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logging.error("Bot stopped!")

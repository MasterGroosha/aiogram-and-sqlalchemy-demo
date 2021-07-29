import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.config_loader import Config, load_config
from bot.db.base import Base
from bot.handlers.commands import register_commands
from bot.handlers.callbacks import register_callbacks


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="play", description="Start a new game (your current score will reset)"),
        BotCommand(command="top", description="View top-5 players scoreboard")
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    config: Config = load_config()
    engine = create_async_engine(
        f"postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.db_name}",
        future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    bot = Bot(config.bot.token, parse_mode="HTML")
    bot["db"] = async_sessionmaker
    dp = Dispatcher(bot)

    register_commands(dp)
    register_callbacks(dp)

    await set_bot_commands(bot)

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

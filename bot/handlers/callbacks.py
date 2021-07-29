from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.utils.exceptions import MessageNotModified
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.common import cb_balls
from bot.keyboards import generate_balls
from bot.db.models import PlayerScore


async def miss(call: types.CallbackQuery):
    """
    Invoked on red ball tap

    :param call: CallbackQuery from Telegram
    """
    db_session = call.bot.get("db")

    async with db_session() as session:
        await session.merge(PlayerScore(user_id=call.from_user.id, score=0))
        await session.commit()

    with suppress(MessageNotModified):
        await call.message.edit_text("Your score: 0", reply_markup=generate_balls())
    await call.answer()


async def hit(call: types.CallbackQuery):
    """
    Invoked on green ball tap

    :param call:CallbackQuery from Telegram
    """
    db_session = call.bot.get("db")

    async with db_session() as session:
        player: PlayerScore = await session.get(PlayerScore, call.from_user.id)
        # Note: we're incrementing client-side, not server-side
        player.score += 1
        await session.commit()

    # Since we have "expire_on_commit=False", we can use player instance here
    with suppress(MessageNotModified):
        await call.message.edit_text(f"Your score: {player.score}", reply_markup=generate_balls())
    await call.answer()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(miss, cb_balls.filter(color="red"))
    dp.register_callback_query_handler(hit, cb_balls.filter(color="green"))

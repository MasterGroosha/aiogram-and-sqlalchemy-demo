from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.common import BallsCallbackFactory
from bot.db.models import PlayerScore
from bot.keyboards import generate_balls

router = Router(name="callbacks-router")


@router.callback_query(BallsCallbackFactory.filter(F.color == "red"))
async def cb_miss(callback: CallbackQuery, session: AsyncSession):
    """
    Invoked on red ball tap
    :param callback: CallbackQuery from Telegram
    :param session: DB connection session
    """

    await session.merge(PlayerScore(user_id=callback.from_user.id, score=0))
    await session.commit()

    with suppress(TelegramBadRequest):
        await callback.message.edit_text("Your score: 0", reply_markup=generate_balls())


@router.callback_query(BallsCallbackFactory.filter(F.color == "green"))
async def cb_hit(callback: CallbackQuery, session: AsyncSession):
    """
    Invoked on green ball tap
    :param callback:CallbackQuery from Telegram
    :param session: DB connection session
    """
    db_query = await session.execute(select(PlayerScore).filter_by(user_id=callback.from_user.id))
    player: PlayerScore = db_query.scalar()
    # Note: we're incrementing client-side, not server-side
    player.score += 1
    await session.commit()

    # Since we have "expire_on_commit=False", we can use player instance here
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(f"Your score: {player.score}", reply_markup=generate_balls())

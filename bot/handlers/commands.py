from aiogram import Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import PlayerScore
from bot.keyboards import generate_balls

router = Router(name="commands-router")


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Handles /start command
    :param message: Telegram message with "/start" text
    """
    await message.answer(
        "Hi there! This is a simple clicker bot. Tap on green ball, but don't tap on red ones!\n"
        "If you tap a red ball, you'll have to start over.\n\n"
        "Enough talk. Just tap /play and have fun!"
    )


@router.message(Command("play"))
async def cmd_play(message: Message, session: AsyncSession):
    """
    Handles /play command
    :param message: Telegram message with "/play" text
    :param session: DB connection session
    """
    await session.merge(PlayerScore(user_id=message.from_user.id, score=0))
    await session.commit()

    await message.answer("Your score: 0", reply_markup=generate_balls())


@router.message(Command("top"))
async def cmd_top(message: Message, session: AsyncSession):
    """
    Handles /top command. Show top 5 players
    :param message: Telegram message with "/top" text
    :param session: DB connection session
    """
    sql = select(PlayerScore).order_by(PlayerScore.score.desc()).limit(5)
    text_template = "Top 5 players:\n\n{scores}"
    top_players_request = await session.execute(sql)
    players = top_players_request.scalars()

    score_entries = [f"{index+1}. ID{item.user_id}: {html.bold(item.score)}" for index, item in enumerate(players)]
    score_entries_text = "\n".join(score_entries)\
        .replace(f"{message.from_user.id}", f"{message.from_user.id} (it's you!)")
    await message.answer(text_template.format(scores=score_entries_text), parse_mode="HTML")

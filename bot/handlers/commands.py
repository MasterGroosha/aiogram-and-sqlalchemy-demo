from aiogram import types, Dispatcher
from sqlalchemy import select

from bot.db.models import PlayerScore
from bot.keyboards import generate_balls


async def cmd_start(message: types.Message):
    await message.answer("Hi there! This is a simple clicker bot. Tap on green ball, but don't tap on red ones!\n"
                         "If you tap a red ball, you'll have to start over.\n\n"
                         "Enough talk. Just tap /play and have fun!")


async def cmd_play(message: types.Message):
    db_session = message.bot.get("db")
    sql = select(PlayerScore).where(PlayerScore.user_id == message.from_user.id)

    async with db_session() as session:
        player_request = await session.execute(sql)
        player = player_request.scalar()
        if not player:
            player = PlayerScore()
            player.user_id = message.from_user.id
        player.score = 0
        session.add(player)
        await session.commit()

    await message.answer("Your score: 0", reply_markup=generate_balls())


def register_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_play, commands="play")

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


async def cmd_top(message: types.Message):
    db_session = message.bot.get("db")
    sql = select(PlayerScore).order_by(PlayerScore.score.desc()).limit(5)
    text_template = "Top 5 players:\n\n{scores}"
    async with db_session() as session:
        top_players_request = await session.execute(sql)
        players = top_players_request.scalars()

    score_entries = [f"{index+1}. ID{item.user_id}: <b>{item.score}</b>" for index, item in enumerate(players)]
    score_entries_text = "\n".join(score_entries)\
        .replace(f"{message.from_user.id}", f"{message.from_user.id} (it's you!)")
    await message.answer(text_template.format(scores=score_entries_text), parse_mode="HTML")



def register_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_play, commands="play")
    dp.register_message_handler(cmd_top, commands="top")

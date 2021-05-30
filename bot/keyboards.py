from random import randint
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.common import cb_balls


def generate_balls() -> InlineKeyboardMarkup:
    balls_mask = [False] * 9
    balls_mask[randint(0, 8)] = True
    balls = ["🔴", "🟢"]
    data = ["red", "green"]
    kb = InlineKeyboardMarkup(row_width=3)
    buttons = [
        InlineKeyboardButton(
            text=balls[item],
            callback_data=cb_balls.new(color=data[item])
        ) for item in balls_mask
    ]
    kb.add(*buttons)
    return kb

from aiogram.filters.callback_data import CallbackData


class BallsCallbackFactory(CallbackData, prefix="ball"):
    color: str


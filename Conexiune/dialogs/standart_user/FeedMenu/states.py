from aiogram.fsm.state import StatesGroup, State


class FeedSG(StatesGroup):
    settings = State()
    w1 = State()
    w2 = State()

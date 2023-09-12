from aiogram.fsm.state import StatesGroup, State


class FeedSG(StatesGroup):
    settings = State()
    setts_sex = State()
    setts_age = State()
    min_age = State()
    max_age = State()
    setts_location = State()
    w1 = State()
    w2 = State()

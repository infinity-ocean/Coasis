from aiogram.fsm.state import StatesGroup, State


class ProfSG(StatesGroup):
    main = State()
    photo = State()
    name = State()
    age = State()
    sex = State()
    loc = State()
    descr = State()

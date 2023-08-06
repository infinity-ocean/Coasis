from aiogram.fsm.state import StatesGroup, State


class ProfMenuSG(StatesGroup):
    main = State()
    photo = State()
    name = State()
    age = State()
    sex = State()
    loc = State()
    descr = State()

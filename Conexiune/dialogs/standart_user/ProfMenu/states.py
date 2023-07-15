from aiogram.fsm.state import StatesGroup, State


class ProfMenuSG(StatesGroup):
    main = State()
    # todo photo = State()
    name = State()
    # todo geo = State()
    descr = State()

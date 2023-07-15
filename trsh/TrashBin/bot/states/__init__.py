from aiogram.fsm.state import StatesGroup, State


class ChatSG(StatesGroup):
    type_product_await = State()
    size_product_await = State()

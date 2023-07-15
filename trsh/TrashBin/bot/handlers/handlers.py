from aiogram import types, F

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from trsh.TrashBin.bot.data import available_products
from trsh.TrashBin.bot.kbd.keyboards import get_row_kbd
from trsh.TrashBin.bot.states import ChatSG

router = Router()


@router.message(CommandStart)
async def start_handler(message: types.Message, state: FSMContext):
    text='Добро пожаловать в БотЭКСПО!\n\n' \
         'Выберите вид блюда:'
    await message.answer(text=text, reply_markup=get_row_kbd(available_products))
    await state.set_state(ChatSG.type_product_await)

@router.message(F.text._in)


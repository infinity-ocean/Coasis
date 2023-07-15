from operator import index

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_row_kbd(product: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in product:
        builder.add(InlineKeyboardButton(text=item, callback_data=item))
    print(builder)
    return builder.as_markup()

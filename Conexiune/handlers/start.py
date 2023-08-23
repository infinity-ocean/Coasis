from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dialogs.standart_user.FeedMenu.states import FeedSG


async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(FeedSG.w1, mode=StartMode.RESET_STACK)

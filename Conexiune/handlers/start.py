from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dialogs.standart_user.menu_dialog import MainMenuSG


async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuSG.hub, mode=StartMode.RESET_STACK)

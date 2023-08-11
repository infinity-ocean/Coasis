from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from Conexiune.dialogs.standart_user.ProfMenu.states import ProfSG


async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ProfSG.main, mode=StartMode.RESET_STACK)

from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from Conexiune.dialogs.standart_user.ProfMenu.states import ProfMenuSG


async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ProfMenuSG.main, mode=StartMode.RESET_STACK)

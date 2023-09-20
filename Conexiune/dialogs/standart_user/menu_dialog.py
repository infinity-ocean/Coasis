from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from dialogs.standart_user.FeedMenu.states import FeedSG
from dialogs.standart_user.ProfMenu.states import ProfSG


class MainMenuSG(StatesGroup):
    hub = State()


main_menu = Dialog(
    Window(
        Const('Эт главная менюшка 😜'),
        Start(Const('Лента🎞'), id='main_feed', state=FeedSG.w1),
        Start(Const('Анкета️✍'), id='main_prof', state=ProfSG.main),
        state=MainMenuSG.hub,
    )
)

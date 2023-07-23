from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Button, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from Conexiune.dialogs.standart_user.ProfMenu.getters import mw_getter, nw_getter, dw_getter
from Conexiune.dialogs.standart_user.ProfMenu.handlers import name_handler, descr_handler
from Conexiune.dialogs.standart_user.ProfMenu.states import ProfMenuSG

main = Window(
    Const('Только что твоя анкета была создана, но она пока пуста. С чего начнём?', when='fresh_created'),
    Const('Твоя анкета пуста. Ты пока что ещё ничего не заполнил.', when='not_filled'),
    Format('{name}\n\n{descr}', when='at_least_one'),
    Group(
        SwitchTo(Const('Имя'), id='to_name', state=ProfMenuSG.name),
        SwitchTo(Const('Описание'), id='descr', state=ProfMenuSG.descr),
        Button(Const('Выложить'), id='send'),
        width=2
    ),
    state=ProfMenuSG.main,
    getter=mw_getter
)

name = Window(
    Const('Имя не введено. Скорее введи его! 4-50 символов.', when='0_name'),
    Format('Твоё имя - {name}.\n\n Если хочешь поменять его, скинь сообщением новое и я его запишу.', when='1_name'),
    MessageInput(name_handler, ContentType.TEXT),
    state=ProfMenuSG.name,
    getter=nw_getter)

descr = Window(
    Const('У тебя пока нету описания. Скорее введи его! 4-50 символов.', when='0_descr'),
    Format('У тебя уже есть описание! Если хочешь его поменять, скинь сообщением новое и я перезапишу\n'
           'Твоё описание - {descr}', when='1_descr'),
    MessageInput(descr_handler, ContentType.TEXT),
    state=ProfMenuSG.descr,
    getter=dw_getter)

prof_dialog = Dialog(main, name, descr)

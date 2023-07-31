from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Button, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from Conexiune.dialogs.standart_user.ProfMenu.getters import mw_getter, nw_getter, dw_getter, sw_getter, pw_getter, \
    aw_getter
from Conexiune.dialogs.standart_user.ProfMenu.handlers import name_handler, descr_handler, m_select, w_select, \
    photo_handler, age_handler
from Conexiune.dialogs.standart_user.ProfMenu.states import ProfMenuSG

main = Window(
    Const('Только что твоя анкета была создана, но она пока пуста. С чего начнём?', when='fresh_created'),
    Const('Твоя анкета пуста. Ты пока что ещё ничего не заполнил.', when='not_filled'),
    DynamicMedia('photo', when='1_photo'),
    Format('{photo_text}\n', when='0_photo'),
    Format('{name}\n\n{age}\n\n{sex}\n\n{descr}', when='at_least_one'),
    Group(
        SwitchTo(Const('Фото'), id='to_photo', state=ProfMenuSG.photo),
        SwitchTo(Const('Имя'), id='to_name', state=ProfMenuSG.name),
        SwitchTo(Const('Возраст'), id='to_age', state=ProfMenuSG.age),
        SwitchTo(Const('Пол'), id='to_sex', state=ProfMenuSG.sex),
        SwitchTo(Const('Описание'), id='to_descr', state=ProfMenuSG.descr),
        Button(Const('Выложить'), id='send'),
        width=2
    ),
    state=ProfMenuSG.main,
    getter=mw_getter
)

photo = Window(
    DynamicMedia('photo', when='1_photo'),
    Const('У тебя пока нету фотографии. Скинь - и я привяжу её к твоей анкете.', when='0_photo'),
    Format('У тебя уже есть фоточка (сверху), если хочешь её поменять - скинь новую.', when='1_photo'),
    MessageInput(photo_handler, ContentType.PHOTO),
    state=ProfMenuSG.photo,
    getter=pw_getter)

name = Window(
    Const('Имя не введено. Скорее введи его! [4-50 символов]', when='0_name'),
    Format('Твоё имя - {name}.\n\n Если хочешь поменять его, скинь сообщением новое и я его запишу.', when='1_name'),
    MessageInput(name_handler, ContentType.TEXT),
    state=ProfMenuSG.name,
    getter=nw_getter)

age = Window(
    Const('Возраст не введён. Скорее введи его!', when='0_age'),
    Format('Твой возраст - {age}.\n\n Если хочешь поменять его, то скинь сообщением новый', when='1_age'),
    MessageInput(age_handler, ContentType.TEXT),
    state=ProfMenuSG.age,
    getter=aw_getter)

sex = Window(
    Const('Выбери свой пол пожалуйста', when='0_sex'),
    Format('Твой пол - {sex}.\n\n Выбери новый если хочешь его поменять', when='1_sex'),
    Group(Button(Const('М'), id='m_sel', on_click=m_select),
          Button(Const('Ж'), id='w_sel', on_click=w_select)),
    state=ProfMenuSG.sex,
    getter=sw_getter)

descr = Window(
    Const('У тебя пока нету описания. Скорее введи его! [10-520 символов]', when='0_descr'),
    Format('У тебя уже есть описание! Если хочешь его поменять, скинь сообщением новое и я перезапишу\n'
           'Твоё описание - {descr}', when='1_descr'),
    MessageInput(descr_handler, ContentType.TEXT),
    state=ProfMenuSG.descr,
    getter=dw_getter)

prof_dialog = Dialog(main, photo, name, age, sex, descr)

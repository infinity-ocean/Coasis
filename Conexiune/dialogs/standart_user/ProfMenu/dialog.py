from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Button, SwitchTo, Cancel
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from dialogs.standart_user.ProfMenu.getters import mw_getter, nw_getter, dw_getter, sw_getter, pw_getter, \
    aw_getter, lw_getter
from dialogs.standart_user.ProfMenu.handlers import name_handler, descr_handler, m_select, w_select, \
    photo_handler, age_handler, send_loc_kbd, loc_handler
from dialogs.standart_user.ProfMenu.states import ProfSG

main = Window(
    Const('Только что твоя анкета была создана, но она пока пуста. С чего начнём?', when='fresh_created'),
    Const('Твоя анкета пуста. Ты пока что ещё ничего не заполнил.', when=
        ~F['photo'] & ~F['name'] & ~F['age'] & ~F['sex'] & ~F['location'] & ~F['descr']
          ),
    DynamicMedia('photo', when='photo'),
    Multi(
        Const('🟡 Ты пока не заполнил фото', when=~F['photo']),
        Const('🟡 Ты пока не заполнил имени', when=~F['name']),
        Format('🟢 Твоё имя - {name}', when='name'),
        Const('🟡 Ты пока не заполнил возраст', when=~F['age']),
        Format('🟢 Твой возраст - {age}', when='age'),
        Const('🟡 Ты пока не заполнил свой пол', when=~F['sex']),
        Format('🟢 Твой пол - {sex}', when='sex'),
        Const('🟡 Ты пока не заполнил свою локацию', when=~F['location']),
        Format('🟢 Твоя локация - {location}', when='location'),
        Const('🟡 Ты пока не заполнил своё описание', when=~F['descr']),
        Format('🟢 Твоё описание - {descr}', when='descr'),
    ),
    Cancel(Const('🧭'), id='p_main_menu'),
    Group(
        SwitchTo(Const('Фото📸'), id='to_photo', state=ProfSG.photo),
        SwitchTo(Const('Имя🎙'), id='to_name', state=ProfSG.name),
        SwitchTo(Const('Возраст🔞'), id='to_age', state=ProfSG.age),
        SwitchTo(Const('Пол🚻'), id='to_sex', state=ProfSG.sex),
        SwitchTo(Const('Локация🗺'), id='to_loc', state=ProfSG.loc),
        SwitchTo(Const('Описание📝'), id='to_descr', state=ProfSG.descr),
        width=4
    ),
    Button(Const('Выложить📩'), id='send'),
    state=ProfSG.main,
    getter=mw_getter
)

photo = Window(
    DynamicMedia('photo', when='photo'),
    Const('У тебя пока нету фотографии. Скинь - и я привяжу её к твоей анкете.', when=~F['photo']),
    Format('У тебя уже есть фоточка (сверху), если хочешь её поменять - скинь новую.', when='photo'),
    MessageInput(photo_handler, ContentType.PHOTO),
    SwitchTo(Const('Назад⬅'), id='to_photo', state=ProfSG.main),
    state=ProfSG.photo,
    getter=pw_getter)

name = Window(
    Const('Имя не введено. Скорее введи его! [4-50 символов]', when=~F['name']),
    Format('Твоё имя - {name}.\n\n Если хочешь поменять его, скинь сообщением новое и я его запишу.', when='name'),
    MessageInput(name_handler, ContentType.TEXT),
    SwitchTo(Const('Назад⬅'), id='to_photo', state=ProfSG.main),
    state=ProfSG.name,
    getter=nw_getter)

age = Window(
    Const('Введи свой возраст, пожалуйста', when=~F['age']),
    Format('Твой возраст - {age}.\n\n Если хочешь поменять его, то скинь сообщением новый', when='age'),
    MessageInput(age_handler, ContentType.TEXT),
    SwitchTo(Const('Назад⬅'), id='to_photo', state=ProfSG.main),
    state=ProfSG.age,
    getter=aw_getter)

sex = Window(
    Const('Выбери свой пол пожалуйста', when=~F['sex']),
    Format('Твой пол - {sex}.\n\n Хочешь сменить? Жмякай на кнопки снизу', when='sex'),
    Group(Button(Const('М‍♂'), id='m_sel', on_click=m_select),
          Button(Const('Ж‍♀'), id='w_sel', on_click=w_select)),
    SwitchTo(Const('Назад⬅'), id='to_photo', state=ProfSG.main),
    state=ProfSG.sex,
    getter=sw_getter)

loc = Window(  # TODO location_text_input
    Const('Тыкни на кнопку и я запишу где ты находишся!', when=~F['loc']),
    Format('Ты находишся тут - {loc}. Отправь свою локацию, если хочешь её поменять', when='loc'),
    MessageInput(loc_handler, ContentType.LOCATION),
    Group(
        Button(Const('Жмякай сюда'), id='loc_kbd', on_click=send_loc_kbd),
        Button(Const('Убрать кнопку снизу'), id='clr_loc_kbd')),
    SwitchTo(Const('Назад⬅'), id='to_photo', state=ProfSG.main),
    state=ProfSG.loc,
    getter=lw_getter
)

descr = Window(
    Const('У тебя пока нету описания. Скорее введи его! [10-520 символов]', when=~F['descr']),
    Format('У тебя уже есть описание! Если хочешь его поменять, скинь сообщением новое и я перезапишу\n'
           'Твоё описание - {descr}', when='descr'),
    MessageInput(descr_handler, ContentType.TEXT),
    SwitchTo(Const('Назад⬅'), id='to_photo', state=ProfSG.main),
    state=ProfSG.descr,
    getter=dw_getter)

prof_dialog = Dialog(main, photo, name, age, sex, loc, descr)

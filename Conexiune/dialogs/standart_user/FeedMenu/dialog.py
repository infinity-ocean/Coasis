from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Multi, Format, Const

from dialogs.standart_user.FeedMenu.getters import getter_w1
from dialogs.standart_user.FeedMenu.states import FeedSG

settings = Window(
    Const('Настрой свою ленту ⬇'),  # todo: make dynamic showing
    Group(
        SwitchTo(Const('Пол'), id='to_sex', state=FeedSG.setts_sex),
        SwitchTo(Const('Возраст'), id='to_age', state=FeedSG.setts_age),
        SwitchTo(Const('Локация'), id='to_location', state=FeedSG.setts_location),
        width=2),
    state=FeedSG.settings,
    # getter=settings_getter
)

setts_sex = Window(
        Const('Фильтр на пол не поставлен.', when=F['sex'] != 'True'),
        Format('Показываю только: {sex}', when='sex'),
        Group(Button(Const('М'), id='m_sel', on_click=m_select_feed),
              Button(Const('Ж'), id='w_sel', on_click=w_select_feed),
              Button(Const('Очистить фильтр'), id='clear_sex', on_click=sex_clear_feed),
              state=FeedSG.setts_sex,
              getter=sw_getter)
)

w1 = Window(
    DynamicMedia('photo', when='photo'),
    Multi(
        Format('{name}', when='name'),
        Format('{age}', when='age'),
        Format('{sex}', when='sex'),
        Format('{location}', when='location'),
        Format('{descr}', when='descr'), sep='\n'
    ),
    Group(
        Button(Const('♥'), id='like', on_click=None),
        SwitchTo(Const('⚙'), id='to_setts', state=FeedSG.settings),
        SwitchTo(Const('⏭'), id='skip', state=FeedSG.w2),
        width=2
    ),
    state=FeedSG.w1,
    getter=getter_w1
)

w2 = Window(
    DynamicMedia('photo', when='photo'),
    Multi(
        Format('{name}', when='name'),
        Format('{age}', when='age'),
        Format('{sex}', when='sex'),
        Format('{location}', when='location'),
        Format('{descr}', when='descr'), sep='\n'
    ),
    Group(
        Button(Const('♥'), id='like', on_click=None),
        SwitchTo(Const('⚙'), id='to_setts', state=FeedSG.settings),
        SwitchTo(Const('⏭'), id='skip', state=FeedSG.w1),
        width=2
    ),
    state=FeedSG.w2,
    getter=getter_w1
)

feed_dialog = Dialog(settings, w1, w2)

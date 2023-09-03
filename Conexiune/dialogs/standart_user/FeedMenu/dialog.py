from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Multi, Format, Const

from dialogs.standart_user.FeedMenu.feed.getters import feed_getter
from dialogs.standart_user.FeedMenu.feed_settings.getters import sex_setts_getter, settings_getter
from dialogs.standart_user.FeedMenu.feed_settings.handlers import set_m_setts, set_w_setts, clear_sex_setts
from dialogs.standart_user.FeedMenu.states import FeedSG

settings = Window(
    Const('Настрой свою ленту ⬇',
          when=(
                  ~F['sex'] & ~F['min_age'] & ~F['max_age'] & ~F['location']
          )),
    Format('Фильтр на пол: {sex}', when='sex'),
    Group(
        SwitchTo(Const('Пол'), id='to_sex', state=FeedSG.setts_sex),
        SwitchTo(Const('Возраст'), id='to_age', state=FeedSG.setts_age),
        SwitchTo(Const('Локация'), id='to_location', state=FeedSG.setts_location),
        width=2),
    state=FeedSG.settings,
    getter=settings_getter
)

setts_sex = Window(
        Const('Фильтр на пол не поставлен.', when=~F['sex']),
        Format('Показываю только: {sex}', when='sex'),
        Group(Button(Const('М'), id='m_slct', on_click=set_m_setts),
              Button(Const('Ж'), id='w_slct', on_click=set_w_setts),
              Button(Const('Очистить фильтр'), id='clear_sex', on_click=clear_sex_setts)),
        state=FeedSG.setts_sex,
        getter=sex_setts_getter
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
    getter=feed_getter
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
    getter=feed_getter
)

feed_dialog = Dialog(settings, setts_sex, w1, w2)

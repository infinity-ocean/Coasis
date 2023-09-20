from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Button, Cancel
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Multi, Format, Const

from dialogs.standart_user.FeedMenu.feed.getters import feed_getter
from dialogs.standart_user.FeedMenu.feed_settings.getters import sex_setts_getter, settings_getter, age_setts_getter
from dialogs.standart_user.FeedMenu.feed_settings.handlers import set_m_setts, set_w_setts, clear_sex_setts, \
    clear_age_setts, age_fs_hndlr
from dialogs.standart_user.FeedMenu.states import FeedSG

settings = Window(
    Const('Настрой свою ленту ⬇',
          when=(
                  ~F['sex'] & ~F['min_age'] & ~F['max_age'] & ~F['location']
          )),
    Multi(
        Format('Фильтр на пол: {sex}', when='sex'),
        Format('Фильтр на пол: не поставлен', when=~F['sex']),
        Multi(Const('Фильтр на возраст: '),
              Format('{min_age}', when='min_age'),
              Const('♾', when=~F['min_age']),
              Const('-'),
              Format('{max_age}', when='max_age'),
              Const('♾', when=~F['max_age']),
              when=F['min_age'] | F['max_age'], sep=''
              ),
        when=F['sex'] | F['min_age'] | F['max_age'] | F['location'],
        sep='\n'
    ),
    Group(
        SwitchTo(Const('Пол'), id='to_sex', state=FeedSG.setts_sex),
        SwitchTo(Const('Возраст'), id='to_age', state=FeedSG.setts_age),
        SwitchTo(Const('Локация'), id='to_location', state=FeedSG.setts_location),
        width=2),
    SwitchTo(Const('Лента'), id='to_feed', state=FeedSG.w1),
    state=FeedSG.settings,
    getter=settings_getter
)

setts_sex = Window(
    Format('Показываю только: {sex}', when='sex'),
    Const('Фильтра на пол нету, но ты всегда можешь его поставить.', when=~F['sex']),
    Group(
        Button(Const('М♂'), id='m_sex_input', on_click=set_m_setts),
        Button(Const('Ж♀'), id='w_sex_input', on_click=set_w_setts),
        Button(Const('Очистить фильтр'), id='clear_sex', on_click=clear_sex_setts),
        SwitchTo(Const('Назад'), id='sex_setts', state=FeedSG.settings)
    ),
    state=FeedSG.setts_sex,
    getter=sex_setts_getter
)

setts_age = Window(
    Format('Минимальный возраст отображения: {min_age}', when='min_age'),
    Format('Максимальный возраст отображения: {max_age}', when='max_age'),
    Const('Минимальный возраст неограничен', when=~F['min_age'] & F['max_age']),
    Const('Максимальный возраст неограничен', when=~F['max_age'] & F['min_age']),
    Const('Фильтр на возраст не поставлен.', when=~F['min_age'] & ~F['max_age']),
    Group(
        Button(Const('Очистить фильтр'), id='clear_sex', on_click=clear_age_setts),
        SwitchTo(Const('Поставить минимум'), id='set_min_age', state=FeedSG.min_age),
        SwitchTo(Const('Поставить максимум'), id='set_max_age', state=FeedSG.max_age),
        SwitchTo(Const('Назад'), id='age_setts', state=FeedSG.settings)
    ),
    state=FeedSG.setts_age,
    getter=age_setts_getter
)

min_age = Window(
    Const('Введи минимальный возраст отображения, пожалуйста'),
    MessageInput(age_fs_hndlr, ContentType.TEXT),
    SwitchTo(Const('Назад'), id='minage_age', state=FeedSG.settings),
    state=FeedSG.min_age,
)

max_age = Window(
    Const('Введи максимальный возраст отображения, пожалуйста'),
    MessageInput(age_fs_hndlr, ContentType.TEXT),
    SwitchTo(Const('Назад'), id='maxage_age', state=FeedSG.settings),
    state=FeedSG.max_age,
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
    Cancel(Const('🧭'), id='w1_menu'),
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
    Cancel(Const('🧭'), id='w2_menu'),
    Group(
        Button(Const('♥'), id='like', on_click=None),
        SwitchTo(Const('⚙'), id='to_setts', state=FeedSG.settings),
        SwitchTo(Const('⏭'), id='skip', state=FeedSG.w1),
        width=2
    ),
    state=FeedSG.w2,
    getter=feed_getter
)

feed_dialog = Dialog(settings, setts_sex, setts_age, min_age, max_age, w1, w2)

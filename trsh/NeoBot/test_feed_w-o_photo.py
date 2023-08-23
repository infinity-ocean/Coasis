import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram_dialog import (
    Dialog, DialogManager, setup_dialogs,
    StartMode, Window,
)
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Group
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const

API_TOKEN = '6130382002:AAE5rwDQZh8D-8wh1QSY9ffju_5yByQtTJ8'


class FeedSG(StatesGroup):
    intro = State()
    settings = State()
    feed = State()


dialog = Dialog(
    Window(
        StaticMedia(url='https://i.imgur.com/9HynSTH.jpeg'),
        Const('Екатерина\n\n'
              '27 лет\n'
              'Ж\n'
              'Санкт-Петербург\n'
              'Рукоделие и не только\n'
              'Всем приветик! Ищу подопытных крысёнышей для моих'
              'фотографических экспериментиков тута.\n\n'
              'Немного страшно было лезть на подобные соцсети,'
              'но мой спиногрыз сказал вылезти сюда,'
              'ведь уже 27 как никак возраст вроде бы уже последних пор,'
              'минувыших дней - невиданной десятилетие узри же'
              'уст моих надежд, о маленькое ты великолепье.\n'
              'И грусть печаль, и грусть тоска одна ж повод это нель.\n'
              'О что за глупая печаль - А ну её, а ну просень!'),
        Group(
            SwitchTo(Const('⚙'), id='to_age', state=FeedSG.settings),
            Button(Const('⭐'), id='to_sex'),
            Button(Const('♥🤝'), id='to_photo'),
            Button(Const('⏭'), id='to_name'),
            width=3
        ),
        state=FeedSG.feed,
    ),
    Window(
    StaticMedia(url='https://i.imgur.com/ddTbbou.png'),
        Const('ФИЛЬТРЫ. От фильтров полностью зависит наполнение ленты.'),
        Row(
            SwitchTo(Const('В меню ↖'), id='to_menu', state=FeedSG.intro),
            SwitchTo(Const('В ленту ↘'), id='to_feed', state=FeedSG.feed)
        ),
        Group(
            Button(Const('🧑👧Пол'), id='to_sex'),
            Button(Const('👴Возраст'), id='to_age'),
            Button(Const('🗺География'), id='to_loc'),
            width=3
        ),
        state=FeedSG.settings
    ),
    Window(
        StaticMedia(url='https://i.imgur.com/ddTbbou.png'),
        Const('МЕНЮ. Дальнейшая навигация происходит отсюда.'),
        Row(
            # SwitchTo(Const('В меню ↖'), id='to_age', state=FeedSG.feed),
            SwitchTo(Const('В ленту ↘'), id='to_age', state=FeedSG.feed)
        ),
        state=FeedSG.intro
    )
)


async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(FeedSG.intro, mode=StartMode.RESET_STACK)


async def main():
    bot = Bot(token='6130382002:AAE5rwDQZh8D-8wh1QSY9ffju_5yByQtTJ8')
    dp = Dispatcher()
    dp.message.register(start, CommandStart())
    dp.include_router(dialog)
    setup_dialogs(dp)

    await dp.start_polling(bot)


asyncio.run(main())

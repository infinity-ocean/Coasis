from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Multi, Format, Const

from dialogs.standart_user.FeedMenu.getters import getter_w1
from dialogs.standart_user.FeedMenu.states import FeedSG

# settings = Window()

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

feed_dialog = Dialog(w1, w2)

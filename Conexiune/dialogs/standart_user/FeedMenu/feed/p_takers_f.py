from datetime import datetime

from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from dialogs.standart_user.FeedMenu.feed.dal_f import get_profiles


async def slct20_handle_back(session: AsyncSession,
                             data: DialogManager.dialog_data,
                             offset=False,
                             pointer=False):
    #### OFFSET+SLCT
    if offset:
        p_list: list = await get_profiles(session, offset=data['offset'])  # TODO: handle p nothing
        data['offset'] += 1
    else:
        p_list: list = await get_profiles(session)  # TODO: handle p nothing
        data['offset'] = 1
    data['profiles'] = []  # CREATION or ANNULMENT
    for p in p_list:
        data['profiles'].append({
            'photo': p.photo, 'name': p.name,
            'age': p.age, 'sex': p.sex,
            'location': p.location, 'descr': p.descr
        })
    data['time_mark'] = datetime.now().timestamp()  # ANNULMENT
    #### POINTER
    if pointer:
        data['pointer'] += 1  # ANNULMENT
    else:
        data['pointer'] = 1
    return p_list[0]


async def slct_p_ram(data: DialogManager.dialog_data):
    try:
        p = data['profiles'][data['pointer']]
        data['pointer'] += 1
        return p
    except:  # TODO: finish
        ...

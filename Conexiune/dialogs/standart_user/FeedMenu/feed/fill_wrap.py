from datetime import datetime

from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.prof_adjust import ProfAdjust
from dialogs.api import to_file_id, get_u_id
from dialogs.standart_user.FeedMenu.db_int import get_profiles, get_setts


async def slct20_handleback(session: AsyncSession,
                            tg_id: int,
                            data: DialogManager.dialog_data,
                            offset: bool = False,
                            ):
    if 'setts' not in data:
        if 'u_id' not in data:
            data['u_id'] = await get_u_id(session, tg_id, data)
        data['setts'] = await get_setts(session, data['u_id'])
    ###--------------------------------------------###
    if offset:
        data['offset'] += 1
    else:
        data['offset'] = 0
    p_list: list = await get_profiles(
        session,
        offset=data['offset'] if offset else None,
        sex=data['setts']['sex'] if 'sex' in data['setts'] else None,
        min_age=data['setts']['min_age'] if 'min_age' in data['setts'] else 18,
        max_age=data['setts']['max_age'] if 'max_age' in data['setts'] else 60,
    )
    ###--------------------------------------------###
    p_0 = p_list[0]  # TODO:Handle: p_list == None
    del p_list[0]
    data['show_list'] = []
    for p in p_list:
        data['show_list'].append({
            'photo': p.photo, 'name': p.name,
            'age': p.age, 'sex': p.sex,
            'location': p.location, 'descr': p.descr
        })
    data['time_mark'] = datetime.now().timestamp()
    return p_0


async def slct_p_ram(data: DialogManager.dialog_data) -> dict:
    p = data['show_list'][0]
    del data['show_list'][0]
    return p


async def wrap_front_dict(p: dict | ProfAdjust):
    if type(p) is dict:
        p_front = {
            'photo': await to_file_id(p['photo']),
            'name': p['name'],
            'age': p['age'],
            'sex': p['sex'],
            'location': p['location'],
            'descr': p['descr'],
        }
    else:
        p_front = {
            'photo': await to_file_id(p.photo),
            'name': p.name,
            'age': p.age,
            'sex': p.sex,
            'location': p.location,
            'descr': p.descr,
        }
    return p_front

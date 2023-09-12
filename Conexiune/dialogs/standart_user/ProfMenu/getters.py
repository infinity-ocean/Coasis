from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from sqlalchemy.ext.asyncio import AsyncSession

from dialogs.standart_user.ProfMenu.mw_getter_api import select_u, registrate_u, fill_front, handle_back


async def mw_getter(**kwargs):
    session: AsyncSession = kwargs['session']
    event = kwargs['event_from_user']
    manager = kwargs['dialog_manager']
    u = await select_u(session, event.id, 'ProfAdjust')
    if not u:
        await registrate_u(session, event, manager.dialog_data)
        return {'fresh_created': True}
    front = await fill_front(u.prof_adj)
    await handle_back(u.prof_adj, manager.dialog_data)
    return front


async def pw_getter(**kwargs):
    if 'photo' not in kwargs['dialog_manager'].dialog_data:
        return {'0_photo': True}
    else:
        img = MediaAttachment(
            ContentType.PHOTO, file_id=MediaId(kwargs['dialog_manager'].dialog_data['photo'])
        )
        return {'photo': img}


async def nw_getter(**kwargs):
    if 'name' not in kwargs['dialog_manager'].dialog_data:
        return {'0_name': True}
    else:
        return {'name': kwargs['dialog_manager'].dialog_data['name']}


async def aw_getter(**kwargs):
    if 'age' not in kwargs['dialog_manager'].dialog_data:  # hide age
        return {'0_age': True}
    else:  # show age
        return {'age': kwargs['dialog_manager'].dialog_data['age']}


async def sw_getter(**kwargs):
    if 'sex' not in kwargs['dialog_manager'].dialog_data:
        return {'0_sex': True}
    else:
        return {'sex': kwargs['dialog_manager'].dialog_data['sex']}


async def lw_getter(**kwargs):
    if 'loc' not in kwargs['dialog_manager'].dialog_data:
        return {'0_loc': True}
    else:
        return {'loc': kwargs['dialog_manager'].dialog_data['loc']}


async def dw_getter(**kwargs):
    if 'descr' not in kwargs['dialog_manager'].dialog_data:
        return {'0_descr': True}
    else:
        return {'descr': kwargs['dialog_manager'].dialog_data['descr']}

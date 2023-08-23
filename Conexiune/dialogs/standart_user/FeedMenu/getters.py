from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from dialogs.standart_user.FeedMenu.getter_api import get_profiles


async def getter_w1(**kwargs):
    manager = kwargs['dialog_manager']

    # Time-check
    # Over-check
    # if await less_4h(redis['time_mark']): 1
    # if redis['pointer'] == 20:
    # before the select -- await get_preferences() --
    if True:  # 1
        if True:
            p_list: list = await get_profiles(kwargs['session'])
            counter = 0
            manager.dialog_data['profiles'] = []
            for p in p_list:
                manager.dialog_data['profiles'].append({
                    'photo': p.photo, 'name': p.name,
                    'age': p.age, 'sex': p.sex,
                    'location': p.location, 'description': p.descr
                })
            p = p_list[0]
            return {
                'photo': MediaAttachment(
                    ContentType.PHOTO, file_id=MediaId(p.photo)
                ),
                'name': p.name,
                'age': p.age,
                'sex': p.sex,
                'location': p.location,
                'descr': p.descr,
            }

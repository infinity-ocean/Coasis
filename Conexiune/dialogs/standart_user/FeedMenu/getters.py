from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from dialogs.standart_user.FeedMenu.getter_api import less_4h
from dialogs.standart_user.FeedMenu.w1_api import slct20_handle_back, slct_p_ram


async def getter_w1(**kwargs):
    dialog_data = kwargs['dialog_manager'].dialog_data

    # before the select -- await get_preferences() -> preferences
    if not 'time_mark' in dialog_data:
        p = await slct20_handle_back(kwargs['session'], dialog_data, offset=False)
    else:
        if await less_4h(dialog_data['time_mark']):
            if dialog_data['pointer'] == 19:
                p = await slct20_handle_back(kwargs['session'], dialog_data, offset=True)
            else:
                p_dict = await slct_p_ram(dialog_data)
                return {
                    'photo': MediaAttachment(ContentType.PHOTO, file_id=MediaId(p_dict['photo'])),
                    'name': p_dict['name'],
                    'age': p_dict['age'],
                    'sex': p_dict['sex'],
                    'location': p_dict['location'],
                    'descr': p_dict['descr'],
                }

        else:
            p = await slct20_handle_back(kwargs['session'], dialog_data, offset=False)
    return {
        'photo': MediaAttachment(ContentType.PHOTO,
                                 file_id=MediaId(p.photo)),
        'name': p.name,
        'age': p.age,
        'sex': p.sex,
        'location': p.location,
        'descr': p.descr,
    }
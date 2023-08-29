from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from dialogs.standart_user.FeedMenu.api_f import less_4h
from dialogs.standart_user.FeedMenu.feed.p_takers_f import slct20_handle_back, slct_p_ram


async def getter_w1(**kwargs):
    dialog_data = kwargs['dialog_manager'].dialog_data

    # TODO!: before the select -- await get_preferences() -> preferences with u_id settle for feed_setts handlers
    if 'time_mark' not in dialog_data:
        p = await slct20_handle_back(kwargs['session'], dialog_data, offset=False)
    else:
        if await less_4h(dialog_data['time_mark']):
            if dialog_data['pointer'] == 19:
                p = await slct20_handle_back(kwargs['session'], dialog_data, offset=True)
            else:  # MAIN FLOW
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
        'photo': MediaAttachment(ContentType.PHOTO, file_id=MediaId(p.photo)),
        'name': p.name,
        'age': p.age,
        'sex': p.sex,
        'location': p.location,
        'descr': p.descr,
    }

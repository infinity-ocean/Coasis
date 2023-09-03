from dialogs.standart_user.FeedMenu.api import less_4h
from dialogs.standart_user.FeedMenu.feed.fill_wrap import slct20_handle_back, slct_p_ram, wrap_front_dict


async def feed_getter(**kwargs):
    tg_id = kwargs['event_from_user'].id
    dialog_data = kwargs['dialog_manager'].dialog_data

    if 'time_mark' in dialog_data:
        if await less_4h(dialog_data['time_mark']):
            if dialog_data['show_list'] is None:
                p = await slct20_handle_back(kwargs['session'], tg_id, dialog_data, offset=True)
            else:  # MAIN FLOW #
                p: dict = await slct_p_ram(dialog_data)
        else:
            p = await slct20_handle_back(kwargs['session'], tg_id, dialog_data)
    else:
        p = await slct20_handle_back(kwargs['session'], tg_id, dialog_data)
    return await wrap_front_dict(p)

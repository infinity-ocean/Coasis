from dialogs.standart_user.FeedMenu.api import more_4h
from dialogs.standart_user.FeedMenu.feed.fill_wrap import slct20_handleback, slct_p_ram, wrap_front_dict


async def feed_getter(**kwargs):
    d_data = kwargs['dialog_manager'].dialog_data
    tg_id = kwargs['event_from_user'].id
    if 'setts_changed' in d_data:
        p = await slct20_handleback(kwargs['session'], tg_id, d_data)  ##1 setts_changed: True
        del d_data['setts_changed']
    elif 'time_mark' in d_data:
        if await more_4h(d_data['time_mark']):
            p = await slct20_handleback(kwargs['session'], tg_id, d_data)  ##2 more_4h: True
        elif 'show_list' in d_data:
            if not d_data['show_list']:
                p = await slct20_handleback(kwargs['session'], tg_id, d_data, ##3 'show_list': None
                                            offset=True)
            else:
                p: dict = await slct_p_ram(d_data) ##4 'show_list' >= 1
    else:
        p = await slct20_handleback(kwargs['session'], tg_id, d_data)  # all is empty
    return await wrap_front_dict(p)
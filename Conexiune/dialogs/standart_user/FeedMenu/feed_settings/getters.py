from sqlalchemy.ext.asyncio import AsyncSession

from dialogs.standart_user.FeedMenu.db_int import get_feed_setts
from dialogs.standart_user.FeedMenu.feed_settings.setts_getter_infra import fill_front, handle_back


async def settings_getter(**kwargs):
    session: AsyncSession = kwargs['session']
    data = kwargs['dialog_manager'].dialog_data
    fs = await get_feed_setts(session, data['u_id'])
    data['new_setts'] = {}
    await handle_back(fs, data['new_setts'])
    if data['setts'] != data['new_setts']:
        data['setts_changed'] = True
    data['setts'] = data['new_setts']
    del data['new_setts']
    return await fill_front(fs)


async def sex_setts_getter(**kwargs):
    data = kwargs['dialog_manager'].dialog_data
    if 'sex' in data['setts']:
        return {'sex': data['setts']['sex']}
    else:
        return {}


async def age_setts_getter(**kwargs):
    setts = kwargs['dialog_manager'].dialog_data['setts']
    front: dict[str, int] = {}
    if 'min_age' in setts:
        front['min_age'] = setts['min_age']
    if 'max_age' in setts:
        front['max_age'] = setts['max_age']
    return front

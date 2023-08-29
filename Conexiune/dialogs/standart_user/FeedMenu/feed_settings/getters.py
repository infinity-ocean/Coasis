from sqlalchemy.ext.asyncio import AsyncSession

from dialogs.standart_user.FeedMenu.feed_settings.api import fill_front, handle_back
from dialogs.standart_user.ProfMenu.mw_getter_api import select_u


async def settings_getter(**kwargs):
    session: AsyncSession = kwargs['session']
    event = kwargs['event_from_user']
    manager = kwargs['dialog_manager']
    u = await select_u(session, event.id, 'FeedSettings')
    await handle_back(u.feed_setts, manager.dialog_data)
    return await fill_front(u.feed_setts)


async def sex_setts_getter(**kwargs):
    data = kwargs['dialog_manager'].dialog_data
    if 'sex' in data:
        return {'sex': data['sex']}
    else:
        return {}

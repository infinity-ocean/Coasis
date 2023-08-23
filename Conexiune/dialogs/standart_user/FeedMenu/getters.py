from dialogs.standart_user.FeedMenu.getter_api import get_profiles


async def getter_w1(**kwargs):
    manager = kwargs['dialog_manager']
    redis = manager.dialog_data
    # Time-check
    # Over-check
    # if await less_4h(redis['time_mark']):
        # await get_preferences()

        # if redis['pointer'] == 20:
    # if not await less_4h(redis['time_mark']):
    if True:

        if True:
            # await get_preferences()
            p_list: list = await get_profiles(kwargs['session'])
            counter = 0
            redis['profiles'] = []
            for p in p_list:
                counter += 1
                nn = {
                    'photo': p.photo, 'name': p.name,
                    'age': p.age, 'sex': p.sex,
                    'location': p.location, 'description': p.descr,
                    'counter': counter
                      }
                redis['profiles'].update(nn)
            p = p_list[0]
            return {
                p.photo, p.name,
                p.age, p.photo,
                p.sex, p.location,
            }

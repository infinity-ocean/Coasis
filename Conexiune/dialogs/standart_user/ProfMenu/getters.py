from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import selectinload

from Conexiune.db.tables.tables import User, ProfAdjust


async def mw_getter(**kwargs):
    #### Variables receiving
    maker: async_sessionmaker[AsyncSession] = kwargs['session_maker']
    event = kwargs['event_from_user']
    manager = kwargs['dialog_manager']
    #### Transaction
    async with maker() as session:
        async with session.begin():
            # necessary data: users.id -> subwindows | users.profadjust | profadjust.*
            slct = select(User).options(selectinload(User.prof_adj)).filter(User.tg_id == event.id)
            raw_u = await session.scalars(slct)
            u = raw_u.one()
            '''user with connected profadj'''
            #### Returning answer to mw with
            #### p:state-filling[0--0.1--1] stat=stat=dyn
            if not u.prof_adj:
                # inserting empty ProfAdjust linked to user creation
                await session.merge(ProfAdjust(user_id=u.id))
                manager.dialog_data['u'] = u
                return {'fresh_created': True}
            p = u.prof_adj  # ТУТА Я ПОДВИНУЛ НА 5 СТРОК МОЖЕТ СЛОМАТЬСЯ
            #### Writing info for subwindows
            manager.dialog_data['u'] = u

    # The prof_adj exists, but is empty
    if not p.name and not p.descr and not p.sex:  # todo + f-a-gl-
        return {'not_filled': True}
    # The prof_adj has at least 1 point
    else:
        widget_filler = {'at_least_one': True}
        if p.name:
            widget_filler['name'] = f'🟢 Твоё имя - {p.name}'
            widget_filler['name_filled'] = True
        else:
            widget_filler['name'] = '🟡 Ты пока не заполнил имени'
            widget_filler['name_filled'] = False
        if p.sex:
            widget_filler['sex'] = f'🟢 Твой пол - {p.sex}'
            widget_filler['sex_filled'] = True
        else:
            widget_filler['sex'] = '🟡 Ты пока не заполнил свой пол'
            widget_filler['sex_filled'] = False
        if p.descr:
            widget_filler['descr'] = f'🟢 Твоё описание - {p.descr}'
            widget_filler['descr_filled'] = True
        else:
            widget_filler['descr'] = '🟡 Ты пока не заполнил описание'
            widget_filler['descr_filled'] = False
        return widget_filler


async def nw_getter(**kwargs):
    # manager = kwargs['dialog_manager']
    dialog_manager = kwargs['dialog_manager']
    u = dialog_manager.dialog_data['u']
    # u.prof_adj = None когда юзер впервые зарег
    if not u.prof_adj:
        return {'0_name': True}
    elif not u.prof_adj.name:
        return {'0_name': True}
    else:
        return {'1_name': True, 'name': u.prof_adj.name}


async def sw_getter(**kwargs):
    manager = kwargs['dialog_manager']
    u = manager.dialog_data['u']
    # u.prof_adj = None когда юзер впервые зарег
    if not u.prof_adj:
        return {'0_sex': True}
    elif not u.prof_adj.sex:
        return {'0_sex': True}
    else:
        return {'1_sex': True, 'sex': u.prof_adj.sex}


async def dw_getter(**kwargs):
    # manager = kwargs['dialog_manager']
    manager = kwargs['dialog_manager']
    u = manager.dialog_data['u']
    # затычка при u; т.к. u.prof_adj = None когда юзер впервые зарег
    if not u.prof_adj:
        return {'0_descr': True}
    elif not u.prof_adj.descr:
        return {'0_descr': True}
    else:
        return {'1_descr': True, 'descr': u.prof_adj.descr}

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
            # todo low|Change to lonely retrieving only ProfAdjust
            # todo edu|to understand this select statement and the result
            stmt = select(User, ProfAdjust).filter(User.tg_id == event.id).options(selectinload(User.prof_adj))
            result_u_profadj = await session.scalars(stmt)
            u = result_u_profadj.all()
            '''user with connected profadj'''
            p = u.prof_adj
            #### Writing info for subwindows
            manager.dialog_data['p_adj'] = p
            manager.dialog_data['u'] = u
            #### Returning answer to mw with
            #### p:state-filling[0=0.1=>1] stat=stat=dyn
            if not p:
                # inserting empty ProfAdjust linked to user creation
                session.add(ProfAdjust(user_id=u.id))
                return {'fresh_created': True}

    # The prof_adj exists, but is empty
    if not p.name and not p.descr:  # + f-aggg-
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
        if p.descr:
            widget_filler['descr'] = f'🟢 Твоё описание - {p.descr}'
            widget_filler['descr_filled'] = True
        else:
            widget_filler['descr'] = '🟡 Ты пока не заполнил описание'
            widget_filler['descr_filled'] = False
        return widget_filler


async def nw_getter(**kwargs):
    manager = kwargs['dialog_manager']
    p = manager.dialog_data['p_adj']
    if not p.name:
        return {'0_name': True}
    else:
        return {'1_name': True, 'name': p.name}

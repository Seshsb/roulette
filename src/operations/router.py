import random

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import Log, Cell
from operations.schemas import Scroll
from users.models import User

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.post('/')
async def scroll(new_scroll: Scroll, session: AsyncSession = Depends(get_async_session)):
    values = new_scroll.dict()
    check_user = await session.execute(select(User).where(User.id == values.get('user_id')))
    if not check_user.scalars().first():
        create_user = insert(User).values({'id': values.get('user_id'), 'round_id': 1})
        await session.execute(create_user)
    round_id = select(User.round_id).where(User.id == values.get('user_id'))
    round_id = await session.execute(round_id)
    values['round_id'] = int(round_id.first()[0])
    list_nums = list(range(1, 11))
    random.shuffle(list_nums)
    for i in list_nums:
        check_jackpot = select(func.count()).select_from(Log).where(
            Log.user_id == values.get('user_id'),
            Log.round_id == values.get('round_id'))
        check_jackpot = await session.execute(check_jackpot)
        if check_jackpot.scalars().first() >= 10:
            await session.execute(
                update(User).values(round_id=values.get('round_id') + 1).where(User.id == values.get('user_id'))
            )
            await session.commit()
            return {'details': "Congratulation, it's jackpot"}

        values['cell_id'] = i
        check_cell = await session.execute(
            select(Log).where(Log.user_id == values.get('user_id'), Log.cell_id == values.get('cell_id'), Log.round_id == values.get('round_id')))
        if not check_cell.scalars().all():
            break
    query = insert(Log).values(**values)
    await session.execute(query)
    weight = select(Cell.weight).where(Cell.id == values.get('cell_id'))
    weight = await session.execute(weight)
    weight = weight.first()[0]
    await session.commit()

    return {'details': {'cell': values.get('cell_id'),
            'weight': weight}}


@router.get('/quantity_users')
async def quantity_users(session: AsyncSession = Depends(get_async_session)):
    quantity_rounds = select(Log.round_id).distinct(Log.round_id)
    quantity_rounds = await session.execute(quantity_rounds)
    quantity_rounds = quantity_rounds.scalars().all()
    resp = {'details': []}
    for round_id in quantity_rounds:
        qnt_users = select(func.count(func.distinct(Log.user_id))).select_from(Log).where(Log.round_id == round_id)
        qnt_users = await session.execute(qnt_users)
        qnt_users = qnt_users.scalars().first()
        resp['details'].append({'round': round_id,
                                'cnt_users': qnt_users})

    return resp


@router.get('/most_active_users')
async def most_active_users(session: AsyncSession = Depends(get_async_session)):
    users = select(Log.user_id).group_by(Log.user_id).order_by(func.count(Log.user_id))
    users = await session.execute(users)
    users = users.scalars().all()
    resp = {'details': []}
    for user in users[::-1]:
        average_scroll = select(func.count()).select_from(Log).where(Log.user_id == user)
        average_scroll = await session.execute(average_scroll)
        average_scroll = average_scroll.scalars().first()
        round_id = select(User.round_id).where(User.id == user)
        round_id = await session.execute(round_id)
        round_id = round_id.scalars().first()
        average_scroll = average_scroll // round_id
        resp['details'].append({
            'user_id': user,
            'round_id': round_id,
            'average_scroll': average_scroll
        })

    return resp



from db.engine import db_session
from db.models import MsgLog
from sqlalchemy import select, update


# Получить сообщение из базы по идентификатору
async def get_msg(tc_msg_id: int):
    async with db_session() as session:
        query = select(MsgLog).where(MsgLog.msg_id == tc_msg_id)

        msg = await session.scalar(query)

        return msg


# Обновить сообщение в базе
async def update_msg(msg: dict, send: int = 1):
    if await get_msg(tc_msg_id=msg.get('id')):
        async with db_session() as session:
            update_values = {
                'from_call_id': msg.get('from_call_id'),
                'from_display_name': msg.get('from_display_name'),
                'time_stamp': msg.get('time_stamp').get('date'),
                'message': msg.get('message'),
                'send': send,
            }
            await session.execute(update(MsgLog).where(MsgLog.msg_id == msg.get('id')).values(update_values))
            await session.commit()
    else:
        await add_msg(msg=msg)


# Добавить сообщение в базу
async def add_msg(msg: dict, send: int = 1):
    async with db_session() as session:
        msg_log = MsgLog(
            msg_id=int(msg.get('id')),
            from_call_id=msg.get('from_call_id'),
            from_display_name=msg.get('from_display_name'),
            time_stamp=msg.get('time_stamp').get('date'),
            message=msg.get('message'),
            send=send,
        )
        session.add(msg_log)
        await session.commit()

        
# Получить последнее сообщение из базы
async def get_last_msg():
    async with db_session() as session:
        query = select(MsgLog).order_by(-MsgLog.id).limit(1)
        
        msg = await session.scalar(query)

        return msg
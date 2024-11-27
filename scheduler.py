from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from trueconf import get_list_chat_messages_text


# Создаем функцию, в которой будет происходить запуск наших тасков.
def set_scheduled_jobs(scheduler, bot, config, *args, **kwargs):
    # Добавляем задачи на выполнение
    scheduler.add_job(transfer_messages_to_chats, "interval", seconds=5, args=(bot, config.bot.chats))


async def transfer_messages_to_chats(bot: Bot, chats: list[int]):
    msg_list = await get_list_chat_messages_text()
    
    for chat in chats:
        for msg in msg_list:
            await bot.send_message(
                chat_id=chat,
                text=msg
            )

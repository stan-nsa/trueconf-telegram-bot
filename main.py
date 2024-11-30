# https://<server>/api/v3.6/logs/messages?access_token=<token>&sort_order=0&to_call_id=<chat-name>&timezone=0&page_size=100&date_from=2024-09-13%2014:00:00

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeDefault, BotCommandScopeAllPrivateChats
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router as handlers_router
from config import config
from db.engine import create_db
import scheduler


async def on_startup():
    print('Start Sibintek Trueconf Telegram Bot')
    await create_db()


async def on_shutdown():
    print('Stop Sibintek Trueconf Telegram Bot')


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    session = AiohttpSession(config.bot.proxy)
    bot = Bot(token=config.bot.token,
              session=session,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    # Удаляем неполученные/необработанные обновления/сообщения
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Шедулер
    scheduler_bot = scheduler.AsyncIOScheduler()
    scheduler.set_scheduled_jobs(scheduler_bot, bot, config)
    scheduler_bot.start()

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        # format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stop Tele-Bot')

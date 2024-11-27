from aiogram import Bot
from aiogram import Router, types
from aiogram.filters import Command

from scheduler import transfer_messages_to_chats
from config import config


router = Router(name=__name__)


@router.message(Command('admin', ignore_case=True))
async def handler_command_admin(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    await message.answer(
        text=f"""
А ты точно Админ? 😏

user id: {user_id}
chat id: {chat_id}
"""
    )

		
@router.message(Command('tc', ignore_case=True))
async def handler_command_tc(message: types.Message, bot: Bot):
    await transfer_messages_to_chats(bot=bot, chats=config.bot.chats)

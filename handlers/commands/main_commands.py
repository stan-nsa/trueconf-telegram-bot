from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
#import keyboards
from help import help_text

router = Router(name=__name__)


# == Обработчик команды /start ====================================================================
@router.message(CommandStart(ignore_case=True))
async def handler_command_start(message: types.Message):
    await message.answer(
        text="""
Это бот для интеграции с чатами TrueConf!
"""
    )
    await message.delete()
# =================================================================================================


# == Обработчик команды /help и кнопки "Помощь" ===================================================
@router.message(Command('help', ignore_case=True))
async def handler_command_help(message: types.Message):
    await message.answer(text=help_text)
    await message.delete()
# =================================================================================================

# URL чтобы узнать id пользователя и id чата: https://api.telegram.org/bot<BOT-TOKEN>/getUpdates
# URL чтобы узнать информацию по апдейтам: https://api.telegram.org/bot<BOT-TOKEN>/getWebhookInfo

from aiogram import Bot
from dataclasses import dataclass
from environs import Env


MSG_TXT_TPL = """
%s (%s):
\t%s
"""


@dataclass
class TgBot:
    token: str              # Токен для доступа к телеграм-боту
    proxy: str              # Прокси
    admins: list[int]       # Список id администраторов бота
    chats: list[int]        # Список id чатов бота
    msg_text_template: str  # Шаблон текста сообщения, пересланного из Trueconf


@dataclass
class DatabaseConfig:
    database: str         # Название базы данных
    db_host: str          # URL-адрес базы данных
    db_user: str          # Username пользователя базы данных
    db_password: str      # Пароль к базе данных


@dataclass
class TrueconfConfig:
    token: str          # Токен для доступа к API
    server: str   # DNS-имя сервера Труконф
    api_adr: str   # адрес API
    chat: str       # Имя чата
	
	
@dataclass
class Config:
    bot: TgBot
    trueconf: TrueconfConfig
    db: DatabaseConfig


env = Env()
env.read_env()


# Создаем экземпляр класса Config и наполняем его данными из переменных окружения
config = Config(
    bot=TgBot(
        token=env('BOT_TOKEN', default=''),
        admins=env.list('ADMINS', subcast=int, default=[]),
        proxy=env('PROXY', default=''),
        chats=env.list('CHATS', subcast=int, default=[]),
        msg_text_template = MSG_TXT_TPL
    ),
    trueconf=TrueconfConfig(
        token=env('TC_API_TOKEN', default=''),
        server=env('TC_SERVER', default=''),
        api_adr=env('TC_API_ADR', default=''),
        chat=env('TC_CHAT', default='')
    ),
    db=DatabaseConfig(
        database=env('DATABASE', default=''),
        db_host=env('DB_HOST', default=''),
        db_user=env('DB_USER', default=''),
        db_password=env('DB_PASSWORD', default='')
    )
)
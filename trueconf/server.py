from .trueconf import Trueconf

from datetime import datetime, timezone, timedelta
import pytz

from config import config

from db import query


# TimeZone
tz = {
    'UTC': pytz.timezone("Europe/London"),
    'MSK': pytz.timezone("Europe/Moscow"),
    'VLAT': pytz.timezone("Asia/Vladivostok"),
}


server = Trueconf(server=config.trueconf.server, api_adr=config.trueconf.api_adr, token=config.trueconf.token, chat=config.trueconf.chat)


async def get_list_chat_messages_text_by_datetime(date_from: str = None):
    messages = server.get_chat_messages_data(date_from=date_from)
    
    msg_list = []
    
    for msg in messages['list']:
        msg_log = await query.get_msg(msg.get('id'))
        if not msg_log:
            dt_str = get_date_time_tz_text(msg.get('time_stamp').get('date'))
            
            msg['time_stamp']['date'] = dt_str
            
            await query.add_msg(msg)
            
            msg_list.append(
                config.bot.msg_text_template % (msg.get('from_display_name'), msg.get('time_stamp').get('date'), msg.get('message'))
            )
        
    return msg_list
    
    
async def get_list_chat_messages_text():
    last_msg = await query.get_last_msg()
    
    msg_list = []
    
    if not last_msg:
        from db.models import MsgLog
        last_msg = MsgLog()
        last_msg.date_time = (datetime.now() - timedelta(minutes=10)).astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        
    msg_list = await get_list_chat_messages_text_by_datetime(last_msg.date_time)
    
    return msg_list

    
def get_date_time_tz_text(dt_str):

    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=timezone.utc)
    
    dtVLAT = dt.astimezone(tz.get('VLAT'))
    
    str = dtVLAT.strftime("%Y-%m-%d %H:%M:%S")

    return str

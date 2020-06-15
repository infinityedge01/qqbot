from os import path, listdir
import datetime
import random
from nonebot import message
setu_path = '/root/data/setu'
setu_list = listdir(setu_path)
last_visit = {}
async def get_a_setu(user_id: int) -> message.MessageSegment:
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(minutes=1)
    
    if user_id in last_visit:
        if last_visit[user_id] + delta > current_time:
            return message.MessageSegment.text('你看太多涩图了')
    last_visit[user_id] = current_time + delta
    cur_setu_path = path.join(setu_path, random.choice(setu_list))
    return message.MessageSegment.image(cur_setu_path)
from os import path, listdir
import datetime
import random
from nonebot import message
from nonebot import log
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
    log.logger.debug(cur_setu_path)
    return message.MessageSegment.image('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1592226374376&di=f8151fbb1876874d55b8c2263cbf6ebf&imgtype=0&src=http%3A%2F%2Fb.hiphotos.baidu.com%2Fzhidao%2Fwh%253D450%252C600%2Fsign%3D14f304ca50da81cb4eb38bc96756fc20%2Fae51f3deb48f8c542d7329113b292df5e0fe7f68.jpg')
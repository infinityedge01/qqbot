from os import path
import asyncio
import datetime
from apscheduler.triggers.date import DateTrigger # 一次性触发器
from nonebot import permission as perm
from nonebot import on_command, CommandSession, scheduler
from nonebot import message
from nonebot import get_bot
from nonebot import log
from .get_setu import *
@on_command('色图', aliases=('涩图'), only_to_me = False)
async def setu(session: CommandSession):
    bot = get_bot()
    if session.current_arg == '':
        has_perm = await perm.check_permission(session.bot, session.event, perm.GROUP)
        if has_perm:
            # msg1 = message.MessageSegment.image('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1592212494831&di=ee6127d25949ab52d82402d2309a8537&imgtype=0&src=http%3A%2F%2Fb.hiphotos.baidu.com%2Fzhidao%2Fwh%253D450%252C600%2Fsign%3D14f304ca50da81cb4eb38bc96756fc20%2Fae51f3deb48f8c542d7329113b292df5e0fe7f68.jpg')
            msg1 = await get_a_setu(session.event.user_id)
            msg_data = await session.send(msg1)
            log.logger.debug(str(msg_data['message_id']))
            # 制作一个“10秒钟后”触发器
            if(msg1 == message.MessageSegment('你看太多涩图了')):
                return
            delta = datetime.timedelta(seconds=10)
            trigger = DateTrigger(
                run_date=datetime.datetime.now() + delta
            )
            scheduler.add_job(
                func=bot.delete_msg,  # 要添加任务的函数，不要带参数
                trigger=trigger,  # 触发器
                kwargs={'message_id':msg_data['message_id'], 'self_id':session.event.self_id},  # 函数的参数列表，注意：只有一个值时，不能省略末尾的逗号
                # kwargs=None,
                misfire_grace_time=1,  # 允许的误差时间，建议不要省略
                # jobstore='default',  # 任务储存库，在下一小节中说明
            )
         #   await asyncio.sleep(10)
         #   await bot.delete_msg(message_id = msg_data['message_id'], self_id = session.event.self_id)
        else:
            msg1 = message.MessageSegment.text('我们可以通过“色图”来表示所有自然界之色，国际照明学会规定分别用x、y、z来表示红、绿、蓝三原色之间的百分比。由于是百分比，三者相加必须等于1，故色调在色图中只需用x、y两值即可。将光谱色中各段波长所引起的色调感觉在x、y平面上做成图标时，即得色图。')
            await session.send(msg1)      
    pass

    
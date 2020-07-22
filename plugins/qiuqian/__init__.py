from os import path, listdir, system
import asyncio
import datetime
import random
from nonebot import permission as perm
from nonebot import on_command, CommandSession, scheduler
from nonebot import message
from nonebot import get_bot
from nonebot import log
is_qiuqian_open = True
from .database import *
bot = get_bot()
db = Database(sys.path[0])
@on_command('开启求签', only_to_me = False, permission = perm.SUPERUSER)
async def open_qiuqian(session):
    if session.current_arg == '':
        global is_qiuqian_open
        is_qiuqian_open = True
        await session.send(message.MessageSegment.text('求签功能已开启'))

@on_command('关闭求签', only_to_me = False, permission = perm.SUPERUSER)
async def close_qiuqian(session):
    if session.current_arg == '':
        global is_qiuqian_open
        is_qiuqian_open = False
        await session.send(message.MessageSegment.text('求签功能已关闭'))

@on_command('求签', aliases=('求籤'), only_to_me = False)
async def setu(session: CommandSession):
    if session.current_arg == '':
        has_perm = await perm.check_permission(session.bot, session.event, perm.GROUP)
        qqid = int(session.event['user_id'])
        if has_perm and is_qiuqian_open:
            Flag = db.can_qiuqian(qqid)
            if Flag: 
                qian = random.randint(1, 100)
                db.change_qian(qqid, qian)
            else: qian = db.get_qian(qqid)
            qianwen = open(path.join(sys.path[0], 'plugins/qiuqian/word/%d.txt' % (qian)))
            str1 = qianwen.read()
            msg0 = message.MessageSegment.at(qqid)
            if Flag:
                msg0 = msg0 + message.MessageSegment.text('\n')
            else:
                msg0 = msg0 + message.MessageSegment.text('今天你已经求过签了\n')
            msg1 = message.MessageSegment.text(str1)
            system('cp -f %s %s' % (path.join(sys.path[0], 'plugins/qiuqian/image/%d.jpg' % (qian)), path.join('/root/coolq/data/image', '%d.jpg' % (qian))))
            msg2 = message.MessageSegment.image('%d.jpg' % (qian))
            await session.send(msg0 + msg1 + msg2)
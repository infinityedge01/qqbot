from os import path
import asyncio
import datetime
import pytz
import requests
import ast
import re
import hashlib
import base64
from apscheduler.triggers.date import DateTrigger # 一次性触发器
from aiocqhttp.exceptions import Error as CQHttpError
from nonebot import permission as perm
from nonebot import on_command, CommandSession, scheduler
from nonebot import message
from nonebot import get_bot
from nonebot import log
from .PCRClanBattle import ClanBattle
Clan = ClanBattle(1314202001949, "2020081016480401600000", "204ea6141f2eed91eb4a3df3d2c1b6e7")
Push_Score_Lines = None
@on_command('查排名', only_to_me = False)
async def query_by_rank(session):
    match = re.match(r'^(\d+)', session.current_arg)
    if not match:
        return
    global Clan
    rank = int(match.group(1))
    if rank <= 0 or rank >= 15000:
        await session.send(message.MessageSegment.text('输入错误'))
        return
    log.logger.debug(str(rank))
    msg_str = Clan.rank_to_string(Clan.get_rank_status(rank), long_info = True)
    await session.send(message.MessageSegment.text(msg_str))

def get_score_line():
    global Clan
    msg_str = ''
    msg_str += Clan.rank_to_string(Clan.get_rank_status(1), long_info = False)
    msg_str += '\n'
    msg_str += Clan.rank_to_string(Clan.get_rank_status(2), long_info = False)
    msg_str += '\n'
    msg_str += Clan.rank_to_string(Clan.get_rank_status(3), long_info = False)
    msg_str += '\n'
    msg_str += Clan.rank_to_string(Clan.get_rank_status(20), long_info = False)
    msg_str += '\n'
    msg_str += Clan.rank_to_string(Clan.get_rank_status(50), long_info = False)
    msg_str += '\n'
    msg_str += Clan.rank_to_string(Clan.get_rank_status(150), long_info = False)
    msg_str += '\n'
    msg_str += Clan.rank_to_string(Clan.get_rank_status(300), long_info = False)
    msg_str += '\n'
    msg_str += Clan.rank_to_string(Clan.get_rank_status(700), long_info = False)
    msg_str += '\n'
    msg_str += Clan.rank_to_string(Clan.get_rank_status(1300), long_info = False)
    return msg_str

@on_command('查档线', only_to_me = False)
async def query_score_line(session):
    if session.current_arg == '':
        msg_str = get_score_line()
        await session.send(message.MessageSegment.text(msg_str))


async def push_score_line_scheduled():
    msg_str = get_score_line()
    bot = get_bot()
    try:
        await bot.send_group_msg(group_id=1038672908, message=message.MessageSegment.text("截至当前的档线：\n") + message.MessageSegment.text(msg_str))
    except CQHttpError:
        pass


@on_command('开启推送档线', only_to_me = False, permission = perm.SUPERUSER)
async def set_open_score_line(session):
    match = re.match(r'^(\d+):(\d+)', session.current_arg)
    if not match:
        return
    hour = int(match.group(1))
    minute = int(match.group(2))
    global Push_Score_Lines
    if Push_Score_Lines != None:
        scheduler.remove_job(Push_Score_Lines)
        Push_Score_Lines = None
    scheduler.add_job(push_score_line_scheduled, 'cron', hour = hour, minute = minute, id = 'score_lines_open')
    Push_Score_Lines = 'score_lines_open'
    await session.send(message.MessageSegment.text('每日{}:{}会自动推送当前档线'.format(str(hour).zfill(2), str(minute).zfill(2))))

@on_command('关闭推送档线', only_to_me = False, permission = perm.SUPERUSER)
async def set_close_score_line(session):
    if session.current_arg == '':
        global Push_Score_Lines
        if Push_Score_Lines != None:
            scheduler.remove_job(Push_Score_Lines)
            Push_Score_Lines = None
        await session.send(message.MessageSegment.text('自动推送当前档线已关闭'))



from os import path
from nonebot import permission as perm
from nonebot import on_command, CommandSession
from nonebot import message
@on_command('色图', aliases=('涩图'), only_to_me = False)
async def setu(session: CommandSession):
    if session.current_arg == '':
        has_perm = await perm.check_permission(session.bot, session.event, perm.SUPERUSER)
        if has_perm:
            msg1 = message.MessageSegment.image('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1592212494831&di=ee6127d25949ab52d82402d2309a8537&imgtype=0&src=http%3A%2F%2Fb.hiphotos.baidu.com%2Fzhidao%2Fwh%253D450%252C600%2Fsign%3D14f304ca50da81cb4eb38bc96756fc20%2Fae51f3deb48f8c542d7329113b292df5e0fe7f68.jpg')
            await session.send(msg1)
        else:
            msg1 = message.MessageSegment.text('我们可以通过“色图”来表示所有自然界之色，国际照明学会规定分别用x、y、z来表示红、绿、蓝三原色之间的百分比。由于是百分比，三者相加必须等于1，故色调在色图中只需用x、y两值即可。将光谱色中各段波长所引起的色调感觉在x、y平面上做成图标时，即得色图。')
            await session.send(msg1)
    pass

    
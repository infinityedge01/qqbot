from os import path
import asyncio
import datetime
import pytz
import re
import sys
import requests
from nonebot import permission as perm
from nonebot import on_command, CommandSession, scheduler
from nonebot import message
from nonebot import get_bot
from nonebot import log

process_headers={
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=09',
	'Connection': 'keep-alive',
	'Content-Length': '115',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Cookie': 'SESS47e98711e78f022e99badf62c8eee3e1=6ff84116dbe3e8be858cdad9f5439cd8; __utmc=46573605; __utmz=46573605152967690911utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=46573605794010901529676548152967654815296790882; __utmt=1; __utmb=465736052101529679088',
	'Host': 'wwwsciweaversorg',
	'Origin': 'http://wwwsciweaversorg',
	'Referer': 'http://wwwsciweaversorg/free-online-latex-equation-editor',
	'User-Agent': 'Mozilla/50 (Windows NT 100; Win64; x64) AppleWebKit/53736 (KHTML, like Gecko) Chrome/670339687 Safari/53736',
	'X-Requested-With': 'XMLHttpRequest',
}

process_url='http://www.sciweavers.org/process_form_tex2img'

@on_command('tex', aliases=('latex'), only_to_me = False, permission = perm.SUPERUSER)
async def tex2img(session):
	tex = session.current_arg
	process_data={
		'eq_latex':tex,
		'eq_bkcolor':'Transparent',
		'eq_font_family':'modern',
		'eq_font':'78',
		'eq_imformat':'JPG',
 	}
	r = requests.post(process_url, headers = process_headers, data = process_data)
	if r.status_code != 200:
		await session.send(message.MessageSegment.text('HTTP ERROR {}'.format(r.status_code)))
	
	num=re.findall(r'Tex2Img_(.*?)/render.png',r.text)
	png_url='http://www.sciweavers.org/upload/Tex2Img_'+num[0]+'/render.png'
	png_html=requests.get(png_url)
	if png_html.status_code == 200:
		with open('plugins/tex2img/tex.png','wb') as pngfile:
			pngfile.write(png_html.content)
		await session.send(message.MessageSegment.image(path.join(sys.path[0], 'plugins/tex2img/tex.png')))


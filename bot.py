from os import path

import nonebot

import config

import asyncio

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.run(
        debug=False,
        use_reloader=False,
        loop=asyncio.get_event_loop(),
    )

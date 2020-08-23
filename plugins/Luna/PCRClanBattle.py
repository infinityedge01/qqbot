import requests
import ast
import hashlib
import base64
import random
from .PCRClient import PCRClient
from nonebot import log
BOSS_LIFE_LIST = [6000000, 8000000, 10000000, 12000000, 20000000]
BOSS_SCORE_MUTIPILE = [[1.0, 1.0, 1.1, 1.1, 1.2], [1.2, 1.2, 1.5, 1.7, 2.0]]
LAP_UPGRADE = [2]
def boss_status(score):
    lap = 1
    boss_id = 0
    ptr = 0
    while True:
        tmp = int(BOSS_LIFE_LIST[boss_id] * BOSS_SCORE_MUTIPILE[ptr][boss_id])
        if score < tmp:
            remaining = int(BOSS_LIFE_LIST[boss_id] - score / BOSS_SCORE_MUTIPILE[ptr][boss_id])
            return lap, boss_id + 1, remaining
        score -= tmp
        boss_id += 1
        if boss_id > 4:
            boss_id = 0
            lap += 1
            if ptr == 0:
                if lap >= LAP_UPGRADE[ptr]: ptr += 1

class ClanBattle:
    def __init__(self, viewer_id, uid, access_key):
        self.uid = uid
        self.access_key = access_key
        self.Client = PCRClient(viewer_id)
        self.Client.login(uid, access_key)
        self.clan_id = 6770
    
    def get_page_status(self, page):
        temp = self.Client.Callapi('clan_battle/period_ranking', {'clan_id': 6770, 'clan_battle_id': -1, 'period': -1, 'month': 0, 'page': page, 'is_my_clan': 0, 'is_first': 1})
        if 'period_ranking' not in temp:
            self.Client.login(self.uid, self.access_key)
            temp = self.Client.Callapi('clan_battle/period_ranking', {'clan_id': 6770, 'clan_battle_id': -1, 'period': -1, 'month': 0, 'page': page, 'is_my_clan': 0, 'is_first': 1})
        return temp['period_ranking']

    def get_rank_status(self, rank):
        temp1 = self.get_page_status((rank - 1) // 10)
        if (rank - 1) % 10 >= len(temp1):
            temp = temp1[(rank - 1) % 10]
        else: temp = {}
        log.logger.debug(str(temp))
        if 'rank' not in temp:
            temp['rank'] = -1
        if 'damage' not in temp:
            temp['damage'] = 0
        if 'clan_name' not in temp:
            temp['clan_name'] = '此行会已解散'
        if 'member_num' not in temp:
            temp['member_num'] = 0
        if 'leader_name' not in temp:
            temp['leader_name'] = 'unknown'
        return temp
    

    def rank_to_string(self, status, long_info = False):
        lap, boss_id, remaining = boss_status(status['damage'])
        
        if long_info:
            return '第{}名：{}，会长：{}，成员数：{}/30，分数：{}，当前进度：{}周目{}王，剩余血量{}/{}'.format(status['rank'], status['clan_name'], status['leader_name'], status['member_num'], status['damage'], lap, boss_id, remaining, BOSS_LIFE_LIST[boss_id - 1])
        else:
            return '第{}名：{}，分数：{}，当前进度：{}周目{}王，剩余血量{}/{}'.format(status['rank'], status['clan_name'], status['damage'], lap, boss_id, remaining, BOSS_LIFE_LIST[boss_id - 1])

#Clan = ClanBattle(1314202001949, "2020081016480401600000", "204ea6141f2eed91eb4a3df3d2c1b6e7")
#print(Clan.rank_to_string(Clan.get_rank_status(102), long_info = True))
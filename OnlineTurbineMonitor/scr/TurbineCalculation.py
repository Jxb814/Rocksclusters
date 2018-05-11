'''
Created on 2018年4月27日
汽轮机热耗率计算
@author: user
'''
from seuif97 import pt2h
import redis
import datetime

conn = redis.Redis('localhost')


class UnitHP:
    def __init__(self, s):
        self.taglist = s.GetTagDefFromExcel()
        self.tagcount = s.tagcount
        self.tagdict = s.desc_valueMatch()
        self.power = self.tagdict['发电机有功功率']
        self.MainSteamFlow = self.tagdict['主蒸汽流量']
        self.MainSteamP = self.tagdict['主蒸汽压力']
        self.MainSteamT = self.tagdict['主蒸汽温度']

        self.RHSteamP = self.tagdict['再热汽压']
        self.RHSteamT = self.tagdict['再热汽温']

        self.FeedwaterFlow = self.tagdict['给水流量']
        self.FeedwaterP = self.tagdict['给水压力']
        self.FeedwaterT = self.tagdict['给水温度']

        self.firstinP = self.tagdict['汽机调速级压力']
        self.firstoutP = self.tagdict['一级抽汽压力']
        self.firstoutT = self.tagdict['一级抽汽温度']
        self.HPoutP = self.tagdict['高压缸排汽压力']       # ~ 二级抽汽压力
        self.HPoutT = self.tagdict['高压缸排汽温度']

        self.SHcoolwaterFlow = self.tagdict['过热器减温水总管流量']
        self.SHcoolwaterP = self.tagdict['过热器减温水总管压力']
        self.SHcoolwaterT = self.tagdict['除氧器水温度']     # ~ 过热器减温水温度

        self.RHcoolwaterFlow = self.tagdict['再热器减温水总管流量']
        self.RHcoolwaterP = self.tagdict['再热器减温水总管压力']
        self.RHcoolwaterT = self.tagdict['再热器减温水温度']

        self.hm = pt2h(self.MainSteamP, self.MainSteamT)        # 主蒸汽焓
        self.hr = pt2h(self.RHSteamP, self.RHSteamT)            # 再热焓
        self.hfw = pt2h(self.FeedwaterP, self.FeedwaterT)       # 给水焓
        self.hcr = pt2h(self.HPoutP, self.firstoutT)            # 冷再热蒸汽焓
        self.hshr = pt2h(self.SHcoolwaterP, self.SHcoolwaterT)  # 过热器减温水焓
        self.hrhs = pt2h(self.RHcoolwaterP, self.RHcoolwaterT)  # 再热器减温水焓
        self.HR = 0
        self.LeakFlow = 1.3707*self.power/300         # 轴封漏汽、阀杆漏汽流量参考设计值
        self.ExtractFlow = 0.1476*self.MainSteamFlow  # 工况变化前后，调节级后通流部分面积不变，抽汽流量与主蒸汽流量为线性关系

    def HeatRateCaculation(self):
        difference = self.LeakFlow/self.MainSteamFlow
        self.RHcoldFlow = self.MainSteamFlow - self.ExtractFlow - self.LeakFlow

        if difference <= 0.005:   # 以主蒸汽流量为基准
            self.RHSteamFlow = self.MainSteamFlow + self.RHcoolwaterFlow - self.ExtractFlow - self.LeakFlow
        else:                     # 以给水流量为基准
            self.RHSteamFlow = self.FeedwaterFlow + self.RHcoolwaterFlow - self.ExtractFlow

        self.HR = (self.MainSteamFlow*self.hm + self.RHSteamFlow*self.hr
                   - self.FeedwaterFlow*self.hfw - self.RHcoldFlow*self.hcr
                   - self.SHcoolwaterFlow*self.hshr - self.RHcoolwaterFlow*self.hrhs)/self.power

        for element in self.taglist:
            if element['desc'] == '热耗率':
                element['value'] = self.HR
                conn.hmset(element['id'], {'value': self.HR, 'ts': datetime.datetime.now()})   # send to redis

        taglist = self.taglist

        return taglist

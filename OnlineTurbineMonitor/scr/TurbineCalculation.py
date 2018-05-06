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
        '''
        self.taglist = s.GetTagDefFromExcel()
        self.tagcount = s.tagcount
        self.tagdict = s.id_valueMatch()
        self.power = self.tagdict['CSDC.DCS2AI.2JZA1200']          # 发电机有功功率
        self.MainSteamFlow = self.tagdict['CSDC.DCS2AI.2JZA1080']  # 主蒸汽流量
        self.MainSteamP = self.tagdict['CSDC.DCS2AI.2JZA1030']     # 主蒸汽压力
        self.MainSteamT = self.tagdict['CSDC.DCS2AI.2JZA2454']     # 主蒸汽温度

        self.RHSteamP = self.tagdict['CSDC.DCS2AI.2JZA2126']    # 再热汽压
        self.RHSteamT = self.tagdict['CSDC.DCS2AI.2JZA0906']    # 再热汽温

        self.FeedwaterFlow = self.tagdict['CSDC.DCS2AI.2JZA0905']  # 给水流量
        self.FeedwaterP = self.tagdict['CSDC.DCS2AI.2JZA2286']     # 给水压力
        self.FeedwaterT = self.tagdict['CSDC.DCS2AI.2JZA1934']     # 给水温度

        self.firstinP = self.tagdict['CSDC.DCS2AI.2JZA0904']    # 调速级压力
        self.firstoutP = self.tagdict['CSDC.DCS2AI.2JZA2238']   # 1级抽汽压力
        self.firstoutT = self.tagdict['CSDC.DCS2AI.2JZA2471']   # 1级抽汽温度
        self.HPoutP = self.tagdict['CSDC.DCS2AI.2JZA2230']      # 高压缸排汽（2级抽汽）压力
        self.HPoutT = self.tagdict['CSDC.DCS2AI.2JZA2463']      # 高压缸排汽温度

        self.SHcoolwaterFlow = self.tagdict['CSDC.DCS2AI.2JZA2166']  # 过热器减温水总管流量
        self.SHcoolwaterP = self.tagdict['CSDC.DCS2AI.2JZA2134']     # 过热器减温水总管压力
        self.SHcoolwaterT = self.tagdict['CSDC.DCS2AI.2JZA2557']     # 过热器减温水温度 ~ 除氧器水温

        self.RHcoolwaterFlow = self.tagdict['CSDC.DCS2AI.2JZA2176']  # 再热器减温水总管流量
        self.RHcoolwaterP = self.tagdict['CSDC.DCS2AI.2JZA2136']     # 再热器减温水总管压力
        self.RHcoolwaterT = self.tagdict['CSDC.DCS2AI.2JZA2074']     # 再热器减温水温度
        '''
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
        '''
        self.RHSteamFlow = self.MainSteamFlow + self.RHcoolwaterFlow - self.ExtractFlow - self.LeakFlow
        self.RHcoldFlow = self.MainSteamFlow - self.ExtractFlow - self.LeakFlow
        self.HR = (self.MainSteamFlow*self.hm + self.RHSteamFlow*self.hr
                   - self.FeedwaterFlow*self.hfw - self.RHcoldFlow*self.hcr
                   - self.SHcoolwaterFlow*self.hshr - self.RHcoolwaterFlow*self.hrhs)/self.power
        if self.taglist[-1]['id'] != 'CSDC.SISCALC.U2_TBHR*':
            self.taglist.append({'desc': u'热耗率', 'id': u'CSDC.SISCALC.U2_TBHR*', 'si': u'kJ/kW.h', 'value': self.HR})
        else:
            self.taglist[-1]['value'] = self.HR
        taglist = self.taglist
        return taglist
        '''
        self.RHSteamFlow = self.MainSteamFlow + self.RHcoolwaterFlow - self.ExtractFlow - self.LeakFlow
        self.RHcoldFlow = self.MainSteamFlow - self.ExtractFlow - self.LeakFlow
        self.HR = (self.MainSteamFlow*self.hm + self.RHSteamFlow*self.hr
                   - self.FeedwaterFlow*self.hfw - self.RHcoldFlow*self.hcr
                   - self.SHcoolwaterFlow*self.hshr - self.RHcoolwaterFlow*self.hrhs)/self.power
        for element in self.taglist:
            if element['desc'] == '热耗率':
                element['value'] = self.HR
                conn.hmset(element['id'],{'value': self.HR, 'ts': datetime.datetime.now()})

        taglist = self.taglist

        return taglist


    def SendToRedisHash(self):
        conn.hmset('CSDC.SISCALC.U2_TBHR*', {'value': self.HR, 'ts': datetime.datetime.now()})


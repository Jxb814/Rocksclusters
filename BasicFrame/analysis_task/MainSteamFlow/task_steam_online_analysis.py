# -*- coding: utf-8 -*-
'''
Created on 2018年4月5日

@author: user
'''
from datetime import datetime
import codecs

from db.pyredis import TagDefToRedisHashKey, tagvalue_redis, SendToRedisHash
from analysis_task.MainSteamFlow.pysteamflow import SteamFlow

class MainSteamFlow:

    def __init__(self, tagin, tagout):
        
        self.ailist = []
   
        file = codecs.open(tagin, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.ailist.append({'id':tagid, 'desc': desc, 'value': float(value)}) 
   
        self.aolist = []
        file = codecs.open(tagout, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.aolist.append({'id':tagid, 'desc':desc, 'value':None, 'ts':None})
                
    def setouttag(self):
        TagDefToRedisHashKey(self.aolist)
        
    def Onlinecal(self):
        RatedState = {}
        RatedState['p'] = 17.154
        RatedState['t'] = 514.73
        RatedState['G'] = 1825.62

        inletstate = {}
        inletstate['p'] = float(self.ailist[0]['value'])
        inletstate['t'] = float(self.ailist[1]['value'])
        
        G = SteamFlow(inletstate, RatedState)
        self.aolist[0]['value'] = G
        return G
                
    def run(self):
       
        tagvalue_redis(self.ailist)
        
        self.Onlinecal()
                
        curtime = datetime.now()
        for tag in self.aolist:
            tag['ts'] = curtime 

        SendToRedisHash(self.aolist)

        tagvalue_redis(self.aolist)
        
        for tag in self.aolist:
            print(tag['desc'], tag['value'])

        
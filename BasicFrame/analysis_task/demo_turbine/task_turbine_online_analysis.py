# -*- coding: utf-8 -*-
"""
    Author:   Cheng Maohua
    Email:    cmh@seu.edu.cn
    License: MIT
"""

from datetime import datetime
import codecs

from db.pyredis import TagDefToRedisHashKey, tagvalue_redis, SendToRedisHash

from analysis_task.demo_turbine.pyturbine import  CylinderEff

class UnitHP:

    def __init__(self, tagin, tagout):
        self.ailist = []
   
        file = codecs.open(tagin, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.ailist.append({'id':tagid, 'desc': desc, 'value': value, 'ts':None}) 
   
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
        pam = float(self.ailist[4]['value']) / 1000     # air pressure
     
        hp = {'inlet':{}, 'outlet':{}, 'h2s':None, 'ef':None}
        minlet = {'p':None, 't': None, 'h': None, 's':None}
        moutlet = {'p': None, 't': None, 'h': None, 's': None}

        minlet['p'] = float(self.ailist[0]['value']) + pam
        minlet['t'] = float(self.ailist[1]['value'])
        moutlet['p'] = float(self.ailist[2]['value']) + pam
        moutlet['t'] = float(self.ailist[3]['value'])

        hp['inlet'] = dict(minlet)
        hp['outlet'] = dict(moutlet)
    
        hp = CylinderEff(hp)
    
        self.aolist[0]['value'] = hp['ef']
    
        return hp
    
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


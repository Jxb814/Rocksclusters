# -*- coding: utf-8 -*-
"""
    Author:   Cheng Maohua
    Email:    cmh@seu.edu.cn
    License: MIT
"""
from db.pyredis import TagDefToRedisHashKey, SendToRedisHash
from datetime import datetime
import random
import codecs

class UnitHPSimulation:

    def __init__(self, tagfile):
        
        self.ailist = []
        file = codecs.open(tagfile, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.ailist.append({'id':tagid, 'desc':desc, 'value':float(value)}) 
      
        self.pibase = self.ailist[0]['value'] 
  
    def settag(self):
        TagDefToRedisHashKey(self.ailist)
 
    def run(self):
        self.ailist[0]['value'] = self.pibase * (1 + random.random() * 0.01)
        
        curtime = datetime.now()
        for tag in self.ailist:
            tag['ts'] = curtime 
        SendToRedisHash(self.ailist)

        print('sampling on ', self.ailist[0]['value'])
 
   

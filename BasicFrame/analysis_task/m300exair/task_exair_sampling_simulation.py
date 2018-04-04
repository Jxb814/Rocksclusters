
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

class UnitExaircoffSimulation:

    def __init__(self, tagfile):
        
        self.ailist = []
        file = codecs.open(tagfile, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.ailist.append({'id':tagid, 'desc':desc, 'value':float(value)}) 
      
        self.o2inbase = self.ailist[0]['value'] 
        self.o2outbase = self.ailist[1]['value'] 
  
    def settag(self):
        TagDefToRedisHashKey(self.ailist)
 
    def run(self):
        self.ailist[0]['value'] = self.o2inbase * (1 + random.random() * 0.01)
        self.ailist[1]['value'] = self.o2outbase * (1 + random.random() * 0.01)
        
        curtime = datetime.now()
        for tag in self.ailist:
            tag['ts'] = curtime 
        SendToRedisHash(self.ailist)

        print('Unit Exaircoff Simulationsampling on ', self.ailist[0]['value'], self.ailist[1]['value'])
 
   

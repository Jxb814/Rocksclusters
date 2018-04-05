# -*- coding: utf-8 -*-
'''
Created on 2018年4月5日

@author: user
'''
from db.pyredis import TagDefToRedisHashKey, SendToRedisHash
from datetime import datetime
import random
import codecs

class MainStreamFlowSimulation:

    def __init__(self, tagfile):
        
        self.ailist = []
        file = codecs.open(tagfile, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.ailist.append({'id':tagid, 'desc':desc, 'value':float(value)}) 
      
        self.pbase = self.ailist[0]['value'] 
        self.tbase = self.ailist[1]['value']
        
    def settag(self):
        TagDefToRedisHashKey(self.ailist)
        
    def run(self):
        self.ailist[0]['value'] = self.pbase* (1 + random.random() * 0.01)
        self.ailist[1]['value'] = self.tbase* (1 + random.random() * 0.01)
        
        curtime = datetime.now()
        for tag in self.ailist:
            tag['ts'] = curtime 
        SendToRedisHash(self.ailist)
        
        print('Main steam flow simulation sampling on ', self.ailist[0]['value'], self.ailist[1]['value'])
 
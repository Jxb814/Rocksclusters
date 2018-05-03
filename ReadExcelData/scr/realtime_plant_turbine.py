# -*- coding: utf-8 -*- 

import redis
import numpy as np

conn = redis.Redis('localhost')

unitnum = 4

rtload = np.zeros(unitnum)
rtqms = np.zeros(unitnum)
rtphpin = np.zeros(unitnum)
rtthpin = np.zeros(unitnum)
rtphpout = np.zeros(unitnum)
rtthpout = np.zeros(unitnum)
rthpe = np.zeros(unitnum)

tagload=['CSDC.DCS1AI.1JZA0209',  #发电机有功功率
         'CSDC.DCS2AI.2JZA1200',
         'CSDC.DCS3AI.3JZA0390',
         'CSDC.DCS4AI.4JZA1247']

tagqms=['CSDC.DCS1AI.1JZA0222',   #主蒸汽流量
        'CSDC.DCS2AI.2JZA1080',
        'CSDC.DCS3AI.3JZA0575',
        'CSDC.DCS4AI.4JZA0779']
     
tagphpin=['CSDC.DCS1AI.1JZA2195',  #主蒸汽压力
          'CSDC.DCS2AI.2JZA2226',
          'CSDC.DCS3AI.3JZA1580',
          'CSDC.DCS4AI.4JZA0672']

tagthpin=['CSDC.DCS1AI.1JZA2339',  #主蒸汽温度
          'CSDC.DCS2AI.2JZA2408',
          'CSDC.DCS3AI.3JZA0830',
          'CSDC.DCS4AI.4JZA0549']
       

tagphpout=['CSDC.DCS1AI.1JZA2199',  #高压缸排汽压力
           'CSDC.DCS2AI.2JZA2230',
           'CSDC.DCS3AI.3JZA1582',
           'CSDC.DCS4AI.4JZA0703']

tagthpout=['CSDC.DCS1AI.1JZA2390',  #高压缸排汽温度
           'CSDC.DCS2AI.2JZA2463',
           'CSDC.DCS3AI.3JZA1682',
           'CSDC.DCS4AI.4JZA0353']

taghpe = ['CSDC.SISCALC.U1_BHEF*',  #高压缸机组内效率
          'CSDC.SISCALC.U2_BHEF*',
          'CSDC.SISCALC.U3_BHEF*',
          'CSDC.SISCALC.U4_BHEF*']

def TagValue(tagid):
    tagvalue=conn.hget(tagid,'value')
    return tagvalue

def realtimedata():
    for i in range(unitnum):
        rtload[i]=float(TagValue(tagload[i]).decode())
       
        rtqms[i]=float(TagValue(tagqms[i]).decode())
        rtphpin[i]=float(TagValue(tagphpin[i]).decode())
        rtthpin[i]=float(TagValue(tagthpin[i]).decode())
        
        rtphpout[i]=float(TagValue(tagphpout[i]).decode())
        rtthpout[i]=float(TagValue(tagthpout[i]).decode())
        rthpe[i]=float(TagValue(taghpe[i]).decode())


# -*- coding: utf-8 -*- 

import numpy as np
import redis

conn = redis.Redis('localhost')

rtload=np.zeros(shape=5)
rthr=np.zeros(shape=5)
rtnhr=np.zeros(shape=5)
rttbsc=np.zeros(shape=5)
rtboef=np.zeros(shape=5)
rtfdcc=np.zeros(shape=5)
rtrcyd=np.zeros(shape=5)
rtgdcm=np.zeros(shape=5)
rtgdcc=np.zeros(shape=5)
rtgdcef=np.zeros(shape=5)

unitnum=4

tagload=['CSDC.SISCALC.U0_LOAD*',
          'CSDC.DCS1AI.1JZA0209',
          'CSDC.DCS2AI.2JZA1200',
          'CSDC.DCS3AI.3JZA0390',
          'CSDC.DCS4AI.4JZA1247']

taghr=['CSDC.SISCALC.U0_HR***',
       'CSDC.SISCALC.U1_TBHR*',
       'CSDC.SISCALC.U2_TBHR*',
       'CSDC.SISCALC.U3_TBHR*',
       'CSDC.SISCALC.U4_TBHR*']

tagnhr=['CSDC.SISCALC.U0_NHR**',
        'CSDC.SISCALC.U1_TBNHR',
        'CSDC.SISCALC.U2_TBNHR',
        'CSDC.SISCALC.U3_TBNHR',
        'CSDC.SISCALC.U4_TBNHR']

tagtbsc=['CSDC.SISCALC.U0_SC***',
         'CSDC.SISCALC.U1_TBSC*',
         'CSDC.SISCALC.U2_TBSC*',
         'CSDC.SISCALC.U3_TBSC*',
         'CSDC.SISCALC.U4_TBSC*']

tagboef=['CSDC.SISCALC.U0_BOEF*',
         'CSDC.SISCALC.U1_BOEF*',
         'CSDC.SISCALC.U2_BOEF*',
         'CSDC.SISCALC.U3_BOEF*',
         'CSDC.SISCALC.U4_BOEF*']

tagfdcc=['CSDC.SISCALC.U0_COAL*',
         'CSDC.SISCALC.U1_FDCC*',
         'CSDC.SISCALC.U2_FDCC*',
         'CSDC.SISCALC.U3_FDCC*',
         'CSDC.SISCALC.U4_FDCC*']

tagrcyd=['CSDC.SISCALC.U0_RCYD*',
         'CSDC.SISCALC.U1_RCYD*',
         'CSDC.SISCALC.U2_RCYD*',
         'CSDC.SISCALC.U3_RCYD*',
         'CSDC.SISCALC.U4_RCYD*']

taggdcm=['CSDC.SISCALC.U0_GDCM*',
         'CSDC.SISCALC.U1_GDCM*',
         'CSDC.SISCALC.U2_GDCM*',
         'CSDC.SISCALC.U3_GDCM*',
         'CSDC.SISCALC.U4_GDCM*']


taggdcc=['CSDC.SISCALC.U0_GDCC*',
         'CSDC.SISCALC.U1_GDCC*',
         'CSDC.SISCALC.U2_GDCC*',
         'CSDC.SISCALC.U3_GDCC*',
         'CSDC.SISCALC.U4_GDCC*']

taggdcef=['CSDC.SISCALC.U0_GDCEF',
          'CSDC.SISCALC.U1_GDCEF',
          'CSDC.SISCALC.U2_GDCEF',
          'CSDC.SISCALC.U3_GDCEF',
          'CSDC.SISCALC.U4_GDCEF']


def TagValue(name):
    tagvalue=conn.hget(name,'value')
    return tagvalue
    
def realtimedata():
    for i in range(unitnum+1):
        rtload[i]=float(TagValue(tagload[i]).decode())
       
        rthr[i]=float(TagValue(taghr[i]).decode())
        rtnhr[i]=float(TagValue(tagnhr[i]).decode())
        
        rttbsc[i]=float(TagValue(tagtbsc[i]).decode())
        
        rtboef[i]=float(TagValue(tagboef[i]).decode())
        rtfdcc[i]=float(TagValue(tagfdcc[i]).decode())
        
        rtrcyd[i]=float(TagValue(tagrcyd[i]).decode())
        
        rtgdcm[i]=float(TagValue(taggdcm[i]).decode())
       
        rtgdcc[i]=float(TagValue(taggdcc[i]).decode())
        rtgdcef[i]=float(TagValue(taggdcef[i]).decode())
   
    rtload[0]= rtload[1]+rtload[2]+rtload[3]+rtload[4] 
    
        
        
        
       

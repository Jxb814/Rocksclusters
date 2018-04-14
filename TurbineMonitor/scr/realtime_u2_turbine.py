# -*- coding: utf-8 -*- 

import redis

conn = redis.Redis('localhost')

tagload={'desc':u'有功功率','name':u'CSDC.DCS2AI.2JZA1200','SI':u'MW','value':'-10000'}
tagqms={'desc':u'主蒸汽流量','name':u'CSDC.DCS2AI.2JZA1080','SI':u't/hW','value':'-10000'}
tagphpin={'desc':u'高压缸进汽压力','name':u'CSDC.DCS2AI.2JZA2226','SI':u'MPa','value':'-10000'}           
tagthpin={'desc':u'高压缸进汽温度','name':u'CSDC.DCS2AI.2JZA2408','SI':u'c','value':'-10000'} 
tagphpout={'desc':u'高压缸排汽压力','name':u'CSDC.DCS2AI.2JZA2230','SI':u'MPa','value':'-10000'}           
tagthpout={'desc':u'高压缸排汽温度','name':u'CSDC.DCS2AI.2JZA2463','SI':u'c','value':'-10000'} 
taghpe={'desc':u'高压缸内效率','name':u'CSDC.DCS2AI.2JZA2226','SI':u'c','value':'-10000'}

def TagValue(name):
    tagvalue=conn.hget(name,'value')
    return tagvalue

def TagSnapshot():
    tagload['value']=TagValue(tagload['name'])
    tagqms['value']=TagValue(tagqms['name'])
    tagphpin['value']=TagValue(tagphpin['name'])
    tagthpin['value']=TagValue(tagthpin['name'])
    tagphpout['value']=TagValue(tagphpout['name'])
    tagthpout['value']=TagValue(tagthpout['name'])
    taghpe['value']=TagValue(taghpe['name'])
    
    print( tagload['value'])

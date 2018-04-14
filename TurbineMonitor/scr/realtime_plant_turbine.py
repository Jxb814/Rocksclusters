
# -*- coding: utf-8 -*- 


import redis

conn = redis.Redis('localhost')

tagload=[{'tagid':'CSDC.DCS1AI.1JZA0209','value':'-10000'},
         {'tagid':'CSDC.DCS2AI.2JZA1200','value':'-10000'},
         {'tagid': 'CSDC.DCS3AI.3JZA0390','value':'-10000'},
         {'tagid':'CSDC.DCS4AI.4JZA1247','value':'-10000'}]

tagqms=[ {'tagid':'CSDC.DCS1AI.1JZA0222','value':'-10000'},
         {'tagid':'CSDC.DCS2AI.2JZA1080','value':'-10000'},
         {'tagid':'CSDC.DCS3AI.3JZA0575','value':'-10000'},
         {'tagid':'CSDC.DCS4AI.4JZA0779','value':'-10000'}]
     
tagphpin=[{'tagid':'CSDC.DCS1AI.1JZA2195','value':'-10000'},
          {'tagid':'CSDC.DCS2AI.2JZA2226','value':'-10000'},
          {'tagid':'CSDC.DCS3AI.3JZA1580','value':'-10000'},
          {'tagid':'CSDC.DCS4AI.4JZA0672','value':'-10000'}]

tagthpin=[{'tagid':'CSDC.DCS1AI.1JZA2339','value':'-10000'},
          {'tagid':'CSDC.DCS2AI.2JZA2408','value':'-10000'},
          {'tagid':'CSDC.DCS3AI.3JZA0830','value':'-10000'},
          {'tagid':'CSDC.DCS4AI.4JZA0549','value':'-10000'}]
       

tagphpout=[{'tagid':'CSDC.DCS1AI.1JZA2199','value':'-10000'},
           {'tagid':'CSDC.DCS2AI.2JZA2230','value':'-10000'},
           {'tagid':'CSDC.DCS3AI.3JZA1582','value':'-10000'},
           {'tagid':'CSDC.DCS4AI.4JZA0703','value':'-10000'}]

tagthpout=[{'tagid':'CSDC.DCS1AI.1JZA2390','value':'-10000'},
           {'tagid':'CSDC.DCS2AI.2JZA2463','value':'-10000'},
           {'tagid':'CSDC.DCS3AI.3JZA1682','value':'-10000'},
           {'tagid':'CSDC.DCS4AI.4JZA0353','value':'-10000'}]

def TagValue(tagid):
    tagvalue=conn.hget(tagid,'value')
    return tagvalue
    
def tagrealtimedata(tag):
    i=0;
    for element in tag:
        tag[i]['value']=TagValue(element['tagid'])
        i=i+1

def realtimedata():
    tagrealtimedata(tagload)
    tagrealtimedata(tagqms)
    tagrealtimedata(tagphpin)
    tagrealtimedata(tagthpin) 
    tagrealtimedata(tagphpout)
    tagrealtimedata(tagthpout)     

realtimedata()      
print(tagqms)  

        
       

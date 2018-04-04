# -*- coding: utf-8 -*-
"""
    Author:   Cheng Maohua
    Email:    cmh@seu.edu.cn
    License: MIT
"""
import redis

conn = redis.Redis('localhost')

def TagDefToRedisHashKey(tagdeflist):  # initialize data to RedisHashKey
    pipe = conn.pipeline()             # do several work at one time
    for element in tagdeflist:
        pipe.hmset(                    # set multiply pairs at the sametime
            element['id'], {'desc': element['desc'], 'value': "-10000", 'ts': ""})
    pipe.execute()


def TagDefFromRedisHash(tagdeflist):   # copy from tegdeflist to taglist
    taglist = []
    for element in tagdeflist:
        htag = conn.hgetall(element['id'])   # get all pairs as form of list
        taglist.append(htag)
    return taglist

def SendToRedisHash(tagvaluelist):     # 
    pipe = conn.pipeline()
    for element in tagvaluelist:
        pipe.hmset(element['id'], {'value': element['value'], 'ts': element['ts']}) #
    pipe.execute()                      # oredered list of value

def tagvalue_redis(taglist):

        tagcount = len(taglist)
        pipe = conn.pipeline()
        for i in range(tagcount):
            pipe.hmget(taglist[i]['id'], 'desc', 'value', 'ts')
        tagvaluelist = pipe.execute()

        for i in range(tagcount):
            taglist[i]['desc'] = tagvaluelist[i][0].decode()
            taglist[i]['value'] = tagvaluelist[i][1].decode()
            taglist[i]['ts'] = tagvaluelist[i][2].decode()



# -*- coding: utf-8 -*-
"""
    Author:   Cheng Maohua
    Email:    cmh@seu.edu.cn
    License: MIT
"""

import json

import redis
import codecs
import os

conn = redis.Redis('localhost')

tagpath = os.path.join(os.path.join(os.path.dirname(__file__), "analysis_task"))

class gentag(object):

    def __init__(self, tagfile):
        self.clients = []
        self.tagfile = tagfile
        self.clients_machine_ip = []
        self.taglist = []

    def GetTagDefInfo(self):
        self.taglist = []
        file = codecs.open(self.tagfile, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                desc, id, si = line.split()
                self.taglist.append({'desc':desc, 'id':id, 'si':si, 'value': '-10000', })

        print(self.taglist)

    def TagSnapshot(self):

        pipe = conn.pipeline()
        for element in self.taglist:
            pipe.hget(element['id'], 'value')

        tagvaluelist = pipe.execute()

        tagvalue = list()
        for element in  tagvaluelist:
            try:
                tagvalue.append(float(element))
            except:
                tagvalue.append(-1000.0)

        return tagvalue


    def gettagdata(self):
        tagvalue = self.TagSnapshot()
        response_to_send = {}
        response_to_send['value'] = tagvalue
        return response_to_send

    def sendmessage2client(self):
        if (len(self.taglist) > 0):
            response_to_send = self.gettagdata()
            for c in self.clients:
                c.write_message(json.dumps(response_to_send))

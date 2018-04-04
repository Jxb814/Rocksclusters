# -*- coding: utf-8 -*-
"""
    Author:   Cheng Maohua
    Email:    cmh@seu.edu.cn
    License: MIT
"""

import tornado.web
import tornado.websocket

import redis

from www.handler.gen_taginfo import gentag

conn = redis.Redis('localhost')

cur_tag = gentag("./handler/m300exair_tag.txt")

class initHandler(tornado.web.RequestHandler):

    def get(self):

        title = '在线监视客户端： 过量空气系数'

        cur_tag.GetTagDefInfo()
        tagvalue = cur_tag.TagSnapshot()

        print('tagvaue', tagvalue)
        print('tagvaue', cur_tag.taglist)
        for i in range(len(tagvalue)):
            cur_tag.taglist[i]['value'] = '{:.2f}'.format(tagvalue[i])

        print(cur_tag.taglist)

        cur_tag.clients_machine_ip.append(self.request.remote_ip)
        print('Client IP:', self.request.remote_ip)

        self.render("m300exair_ui.html", title=title, tagname=cur_tag.taglist)

    def post(self):
        pass

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        print("message received " + message)

    def open(self):
        if self not in cur_tag.clients:
            cur_tag.clients.append(self)
            self.write_message(u"Connected")
            print("WS Clients" + str(len(cur_tag.clients)))

    def on_close(self):
        if self in cur_tag.clients:
            cur_tag.clients.remove(self)
            print("WS Clientse " + str(len(cur_tag.clients)))
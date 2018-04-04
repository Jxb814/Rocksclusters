# -*- coding: utf-8 -*-
"""
    Author:   Cheng Maohua
    Email:    cmh@seu.edu.cn
    License: MIT
"""

import tornado.web
import tornado.websocket

from www.handler.gen_taginfo import gentag

tb_tag = gentag("./handler/demo_turbine_tag.txt")

class initHandler(tornado.web.RequestHandler):

    def get(self):

        title = '在线监视客户端： 高压缸效率'

        tb_tag.GetTagDefInfo()
        tagvalue = tb_tag.TagSnapshot()

        print('tagvaue', tagvalue)
        print('tagvaue', tb_tag.taglist)
        for i in range(len(tagvalue)):
            tb_tag.taglist[i]['value'] = '{:.2f}'.format(tagvalue[i])

        print(tb_tag.taglist)

        tb_tag.clients_machine_ip.append(self.request.remote_ip)
        print('Client IP:', self.request.remote_ip)

        self.render("demo_turbine_ui.html", title=title, tagname=tb_tag.taglist)

    def post(self):
        pass

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        print("message received " + message)

    def open(self):
        if self not in tb_tag.clients:
            tb_tag.clients.append(self)
            self.write_message(u"Connected")
            print("Turbine WS Clients" + str(len(tb_tag.clients)))

    def on_close(self):
        if self in tb_tag.clients:
            tb_tag.clients.remove(self)
            print("Turbine WS Clientse " + str(len(tb_tag.clients)))

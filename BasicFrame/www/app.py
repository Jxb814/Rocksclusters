# -*- coding: utf-8 -*-
"""
    Author:   Cheng Maohua
    Email:    cmh@seu.edu.cn
    License: MIT
"""

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os

import sys
sys.path.append("./")
sys.path.append("..")

import www.handler.demo_turbine_handler as demo_turbine

# TODO: import your handler
import www.handler.m300exair_handler as m300exair
import www.handler.steamrate_handler as steamrate

def sendmessage2allclient():
    demo_turbine.tb_tag.sendmessage2client()

    # TODO: add your task
    m300exair.cur_tag.sendmessage2client()
    steamrate.tb_tag.sendmessage2client()

class indexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [

            (r"/", indexHandler),

            # demo handler
            (r"/demo_tb/", demo_turbine.initHandler),
            (r"/demo_tbwebsocket", demo_turbine.WebSocketHandler),
            

            # TODO: add your handler
            (r"/m300exair/", m300exair.initHandler),
            (r"/m300exair_websocket", m300exair.WebSocketHandler),
            
            (r"/steamrate/", steamrate.initHandler),
            (r"/steamrate_websocket", steamrate.WebSocketHandler)
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )

        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)

    mainLoop = tornado.ioloop.IOLoop.instance()

    scheduler_update = tornado.ioloop.PeriodicCallback(sendmessage2allclient, 2000, io_loop=mainLoop)
    scheduler_update.start()

    print('Web Server started! ')
    mainLoop.start()

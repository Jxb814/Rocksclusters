'''
Created on 2018年4月27日

@author: user
'''
import os
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

import handler.plant_handler as plt
import handler.u1_turbine_handler as u1t
import handler.u2_turbine_handler as u2t

import handler.RedisInfoMonitor_handler as redisinfo
import app_global as glb

import socket


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def sendmessage():
    if (len(plt.clients) > 0):
        plt.sendmessage2client()
    if (len(u1t.clients) > 0):
        u1t.sendmessage2client()
    if (len(u2t.clients) > 0):
        u2t.sendmessage2client()


class indexHandler(tornado.web.RequestHandler):

    def get(self):
        glb.clients_machine_ip.append(self.request.remote_ip)
        print('Client IP:', self.request.remote_ip)
        self.render("index.html")


class App(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", indexHandler),

            (r"/realtime_plant/", plt.realtimeHandler),
            (r"/pltwebsocket", plt.WebSocketHandler),

            (r"/realtime_u1_turbine/", u1t.realtimeHandler),
            (r"/u1twebsocket", u1t.WebSocketHandler),

            (r"/realtime_u2_turbine/", u2t.realtimeHandler),
            (r"/u2twebsocket", u2t.WebSocketHandler),

            (r"/redisinfomonitor/", redisinfo.RedisInfoHandler),
        ]

        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            'static_path': os.path.join(os.path.dirname(__file__), "static")
        }

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = App()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)

    mainLoop = tornado.ioloop.IOLoop.instance()
    scheduler_task = tornado.ioloop.PeriodicCallback(sendmessage, 2000)
    scheduler_task.start()
    print('Web Server start:on %s:8000' % get_host_ip())
    mainLoop.start()

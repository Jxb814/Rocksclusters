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
import handler.u2_turbine_handler as u2t
import handler.RedisInfoMonitor_handler as redisinfo
import app_global as glb


def sendmessage():
    if (len(plt.clients) > 0):
        plt.sendmessage2client()
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
#    tornado.ioloop.IOLoop.instance().start()
    mainLoop = tornado.ioloop.IOLoop.instance()

    scheduler_task = tornado.ioloop.PeriodicCallback(sendmessage, 2000,
                                                     io_loop=mainLoop)
    scheduler_task.start()

    print('Web Server start')
    mainLoop.start()

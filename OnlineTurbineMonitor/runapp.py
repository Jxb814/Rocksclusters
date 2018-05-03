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

import scr.calculation as cal
import scr.data_to_redis as dat

def sendmessage():
    pass

class indexHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("plant.html")
        
class App(tornado.web.Application):
    
    def __init__(self):
        handlers = [
            (r"/", indexHandler),
            (r"realtime_plant", plt.realtimeHandler),
            (r"/realtime_u2_turbine", u2t.realtimeHandler)
        ]
        
        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            'static_path': os.path.join(os.path.dirname(__file__), "static")      
        }
        
        tornado.web.Application.__init__(self, handlers, **settings)
        
if __name__=='__main__':
    tornado.options.parse_command_line()
    app = App()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
#    tornado.ioloop.IOLoop.instance().start()
    mainLoop = tornado.ioloop.IOLoop.instance()
  
    scheduler_task = tornado.ioloop.PeriodicCallback(sendmessage(), 2000, io_loop=mainLoop)
    scheduler_task.start()
    
    print('Web Server start')
    mainLoop.start()    
        
        
import tornado.web
import tornado.httpserver
import tornado.ioloop

import tornado.options

import handler.realtime_plant_performance_handler as RealtimePlantHandler
import handler.realtime_plant_turbine_handler as RealtimeAllTurbineHandler
import handler.realtime_u2_turbine_handler as RealtimeU2TuebineHandler
import handler.RedisInfoMonitor_handler as RedisHandler

client = list() 
        
class aboutHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("about.html")    

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", RealtimePlantHandler.realtimeHandler),
       
            (r"/realtime_plant_performance/", RealtimePlantHandler.realtimeHandler),
            (r"/realtime_plant_turbine/", RealtimeAllTurbineHandler.realtimeHandler),
          
            (r"/realtime_u2_turbine/", RealtimeU2TuebineHandler.realtimeHandler),
         
            (r"/RedisInfoMonitor/", RedisHandler.RedisInfoHandler),
            (r"/about/", aboutHandler)
        ]
        
        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
   


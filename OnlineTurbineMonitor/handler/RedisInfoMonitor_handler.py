import tornado.web
import json

import scr.RedisInfoMonitor as rt

class RedisInfoHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("redisinfomonitor.html")    
 
    def post(self):
        
        response_to_send = rt.RedisInfo()
        self.write(json.dumps(response_to_send))
  



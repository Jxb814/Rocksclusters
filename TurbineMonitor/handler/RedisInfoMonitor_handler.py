import tornado.web
import json
import pprint

import scr.RedisInfoMonitor as rt

class RedisInfoHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("RedisInfoMonitor.html")    
 
    def post(self):
        
        response_to_send=rt.RedisInfo()
     
        print('Response to return')
        pprint.pprint(response_to_send)
    
        self.write(json.dumps(response_to_send))
  



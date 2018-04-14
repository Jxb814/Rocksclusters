import tornado.web
import json
import pprint

import scr.realtime_u2_turbine as rt

class realtimeHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("realtime_u2_turbine.html")    
 
    def post(self):
        
        rt.TagSnapshot()
            # new dictionary
        response_to_send = {}
         
        response_to_send['load'] =float(rt.tagload['value'].decode())
        response_to_send['qms'] =float(rt.tagqms['value'].decode())
        response_to_send['phpin'] =float(rt.tagphpin['value'].decode())
        response_to_send['thpin'] =float(rt.tagthpin['value'].decode())
        response_to_send['phpout'] =float(rt.tagphpout['value'].decode())
        response_to_send['thpout'] =float(rt.tagthpout['value'].decode())
        response_to_send['hpe'] =float(rt.taghpe['value'].decode())
    
        print('Response to return')
        pprint.pprint(response_to_send)
    
        self.write(json.dumps(response_to_send))
  



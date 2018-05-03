import tornado.web
import json
import pprint

import scr.realtime_plant_turbine as rt

index = 2
class realtimeHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("realtime_u2_turbine.html")    
 
    def post(self):
        
        rt.realtimedata()
            # new dictionary
        response_to_send = {}

        response_to_send['load'] =float(rt.rtload[index-1])
        response_to_send['qms'] =float(rt.rtqms[index-1])
        response_to_send['phpin'] =float(rt.rtphpin[index-1])
        response_to_send['thpin'] =float(rt.rtthpin[index-1])
        response_to_send['phpout'] =float(rt.rtphpout[index-1])
        response_to_send['thpout'] =float(rt.rtthpout[index-1])
        response_to_send['hpe'] =float(rt.rthpe[index-1])
    
        print('Response to return')
        pprint.pprint(response_to_send)
    
        self.write(json.dumps(response_to_send))
  



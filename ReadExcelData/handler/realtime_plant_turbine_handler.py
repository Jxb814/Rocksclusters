import tornado.web
import json
import pprint

import scr.realtime_plant_turbine as rt

class realtimeHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("realtime_plant_turbine.html")    
 
    def post(self):
        
        rt.realtimedata()
            # new dictionary
        response_to_send = {}
      
        received_data = list()
        for i in range(rt.unitnum):
            received_data.append(rt.rtload[i])
        response_to_send['load'] =received_data
    
        received_data = list()
        for i in range(rt.unitnum):
            received_data.append(rt.rtqms[i])
        response_to_send['qms'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum):
            received_data.append(rt.rtphpin[i])
        response_to_send['phpin'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum):
            received_data.append(rt.rtthpin[i])
        response_to_send['thpin'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum):
            received_data.append(rt.rtphpout[i])
        response_to_send['phpout'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum):
            received_data.append(rt.rtthpout[i])
        response_to_send['thpout'] =received_data
       
       
        print('Response to return')
        pprint.pprint(response_to_send)
    
        self.write(json.dumps(response_to_send))  


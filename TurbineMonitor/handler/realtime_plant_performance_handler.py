import tornado.web
import json
import pprint

import scr.realtime_plant_performance as rt

class realtimeHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("realtime_plant_performance.html")    
 
    def post(self):
        
        rt.realtimedata()
            # new dictionary
        response_to_send = {}
      
        received_data = list()
        for i in range(rt.unitnum+1):
            received_data.append(rt.rtload[i])
        response_to_send['load'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum+1):
            received_data.append(rt.rthr[i])
        response_to_send['hr'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum+1):
            received_data.append(rt.rtnhr[i])
        response_to_send['nhr'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum+1):
            received_data.append(rt.rttbsc[i])
        response_to_send['tbsc'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum+1):
            received_data.append(rt.rtboef[i])
        response_to_send['boef'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum+1):
            received_data.append(rt.rtfdcc[i])
        response_to_send['fdcc'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum+1):
            received_data.append(rt.rtrcyd[i])
        response_to_send['rcyd'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum+1):
            received_data.append(rt.rtgdcc[i])
        response_to_send['gdcc'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum+1):
            received_data.append(rt.rtgdcm[i])
        response_to_send['gdcm'] =received_data
        
        received_data = list()
        for i in range(rt.unitnum+1):
            received_data.append(rt.rtgdcef[i])
        response_to_send['gdcef'] =received_data
        
      
        
        print('Response to return')
        pprint.pprint(response_to_send)
    
        self.write(json.dumps(response_to_send))  


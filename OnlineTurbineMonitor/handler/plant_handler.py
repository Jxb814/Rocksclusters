'''
Created on 2018年4月27日

@author: user
'''
import tornado.web
import tornado.websocket
import json

import scr.plant as rt

clients_machine_ip = []
clients_monitor_count = 0
rhclients = []

rowindex = 2
coldescindex = 1
colsiindex = 3
colnameindex = 2
by_name = u'PLANT'
s = rt.generalsheet('./cs_tag_all.xlsx', rowindex,
                    colnameindex, colsiindex, coldescindex, by_name)


def rh_gettagdata():
    tagvaluelist = s.Tagsnapshot()
    response_to_send = {}
    response_to_send['value'] = tagvaluelist
    return response_to_send


def sendmessage2client():
    response_to_send = rh_gettagdata()
    for c in rhclients:
        c.write_message(json.dumps(response_to_send))  # python->json data structure


class realtimeHandler(tornado.web.RequestHandler):

    def get(self):
        title = '全厂热力系统性能概况'
        self.tagname = s.GetTagDefFromExcel()

        clients_machine_ip.append(self.request.remote_ip)
        print('Client IP:', self.request.remote_ip)

        self.render("realtime_rh_d3_ws.html", title=title,
                    tagname=self.tagname)

    def post(self):
        pass


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        print("message received" + message)

    def open(self):
        if self not in rhclients:
            rhclients.append(self)
            self.write_message(u"connected")
            clients_monitor_count += 1
            print("PlantRH WS open" + str(len(rhclients)) +
                  "Total Client: ", str(clients_monitor_count))

    def on_close(self):
        if self in rhclients:
            rhclients.remove(self)
            clients_monitor_count -= 1
            print("PlantRH WS close" + str(len(rhclients)) +
                  "Total Client: ", str(clients_monitor_count))

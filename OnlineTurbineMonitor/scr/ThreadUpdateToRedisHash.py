# -*- coding: utf-8 -*-

import threading
import datetime
import time
import redis
import xlrd

conn = redis.Redis('localhost')


class PeriodicSensor ():

    def __init__(self, delay, file, rowindex, colidindex, colvalueindex, sheet_name):
        self.next_call = time.time()   # seconds
        self.delay = delay
        self.excelfile = self.open_excel(file)
        self.rowindex = rowindex
        self.colidindex = colidindex
        self.colvalueindex = colvalueindex
        self.sheet = self.excelfile.sheet_by_name(sheet_name)
        self.nrows = self.sheet.nrows
        self.taglist = self.tagname_from_excel()
        self.sheetname = sheet_name
        print(self.sheetname)

    def open_excel(self, file):
        try:
            data = xlrd.open_workbook(file)
            return data
        except Exception as e:
            print (e)

    def tagname_from_excel(self):
        taglist = []
        for rownum in range(self.rowindex, self.nrows):
            tagdef = {'id': u'', 'value': '', 'ts': ''}
            tagdef['id'] = self.sheet.cell(rownum, self.colidindex).value
            taglist.append(tagdef)
        return taglist

    def tagvalue_from_excel(self):
        taglist = []
        for rownum in range(self.rowindex, self.nrows):
            tagdef = {'id': u'', 'value': '', 'ts': ''}
            tagdef['id'] = self.sheet.cell(rownum, self.colidindex).value
            tagdef['value'] = self.sheet.cell(rownum, self.colvalueindex).value
            taglist.append(tagdef)

        if self.sheetname == 'DCS1AI':         # 循环读取F5和H7的值
                if self.colvalueindex == 5:
                    self.colvalueindex = 7
                elif self.colvalueindex == 7:
                    self.colvalueindex = 5

        if self.sheetname == 'DCS2AI':         # 循环读取G6-AE30的值
                self.colvalueindex = self.colvalueindex + 1
                if self.colvalueindex > 30:
                    self.colvalueindex = 6

        return taglist

    def SendToRedisHash(self):
        tagvaluelist = self.tagvalue_from_excel()

        curtime = datetime.datetime.now()   # date & time

        pipe = conn.pipeline()
        for element in tagvaluelist:
            pipe.hmset(element['id'], {'value': element['value'], 'ts': curtime})
#           print(type(element['value']))
        pipe.execute()

#        print(tagvaluelist[0])
#        print(conn.hmget(tagvaluelist[0]['id'], 'value'))

    def worker(self):
        self.SendToRedisHash()
        self.next_call = self.next_call + self.delay
        threading.Timer(self.next_call - time.time(), self.worker).start()


def ThreadUpdateBegin(filename, rowindex, colidindex, colvalueindex, sheet_name):
    Sensor = PeriodicSensor(2, filename, rowindex, colidindex,
                            colvalueindex, sheet_name)
    Sensor.worker()


'''
if __name__ == "__main__":

    rowindex = 2
    colidindex = 2
    colvalueindex = 5  # F5列

    SensorU1AI = PeriodicSensor(2, u'./cs_tag_all.xlsx', rowindex,
                                colidindex, colvalueindex, u'DCS1AI')
    SensorU1AI.worker()

    SensorU1CO = PeriodicSensor(2, u'./cs_tag_all.xlsx', rowindex,
                                colidindex, colvalueindex, u'1CAL')
    SensorU1CO.worker()

    colvalueindex = 6  # G6列
    SensorU2AI = PeriodicSensor(2, u'./cs_tag_all.xlsx', rowindex,
                                colidindex, colvalueindex, u'DCS2AI')
    SensorU2AI.worker()

    colvalueindex = 5  # F5列
    SensorU2CO = PeriodicSensor(2, u'./cs_tag_all.xlsx', rowindex,
                                colidindex, colvalueindex, u'2CAL')
    SensorU2CO.worker()

    SensorU3AI = PeriodicSensor(2, u'./cs_tag_all.xlsx', rowindex,
                                colidindex, colvalueindex, u'DCS3AI')
    SensorU3AI.worker()

    SensorU3CO = PeriodicSensor(2, u'./cs_tag_all.xlsx', rowindex,
                                colidindex, colvalueindex, u'3CAL')
    SensorU3CO.worker()

    SensorU4AI = PeriodicSensor(2, u'./cs_tag_all.xlsx', rowindex,
                                colidindex, colvalueindex, u'DCS4AI')
    SensorU4AI.worker()

    SensorU4CO = PeriodicSensor(2, u'./cs_tag_all.xlsx', rowindex,
                                colidindex, colvalueindex, u'4CAL')
    SensorU4CO.worker()

    SensorPLTCO = PeriodicSensor(2, u'./cs_tag_all.xlsx', rowindex,
                                 colidindex, colvalueindex, u'PLANT')
    SensorPLTCO.worker()
    
'''

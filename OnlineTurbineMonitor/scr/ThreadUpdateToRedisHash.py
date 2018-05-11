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
        pipe.execute()

    def worker(self):
        self.SendToRedisHash()
        self.next_call = self.next_call + self.delay
        threading.Timer(self.next_call - time.time(), self.worker).start()


def ThreadUpdateBegin(filename, rowindex, colidindex, colvalueindex, sheet_name):
    Sensor = PeriodicSensor(2, filename, rowindex, colidindex,
                            colvalueindex, sheet_name)
    Sensor.worker()

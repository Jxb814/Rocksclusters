# -*- coding: utf-8 -*- 

import threading
from  datetime  import  *
import time
import redis
import xlrd

conn = redis.Redis('localhost')

class PeriodicSensor ():
  
    def __init__ (self, delay,file,rowbegindex,colidindex,coldescindex,colvalueindex,sheet_name):
        self.next_call = time.time()   # seconds
        self.delay = delay
        
        self.excelfile=self.open_excel(file)
        self.sheetname=sheet_name
        
        self.rowbegindex=rowbegindex
        self.colidindex=colidindex
        self.colvalueindex=colvalueindex
        self.coldescindex=coldescindex
        
        self.sheet = self.excelfile.sheet_by_name(sheet_name)
        self.nrows = self.sheet.nrows
        
        self.taglist=self.tag_from_excel()

        print(self.sheetname)
      
    def open_excel(self,file):
        try:
            data = xlrd.open_workbook(file)
            return data
        except Exception as e:
            print (e)

    def tag_from_excel(self):
        taglist = []
        for rownum in range(self.rowbegindex,self.nrows):
            tag ={'id':u'','desc':u'','value':'','ts':''}
            tag['id']=self.sheet.cell(rownum,self.colidindex).value
            tag['desc']=self.sheet.cell(rownum,self.coldescindex).value
            tag['value']=self.sheet.cell(rownum,self.colvalueindex).value
            taglist.append(tag)
      
        if self.sheetname=='DCS1AI':         # 循环读取F5和H7的值
                if self.colvalueindex==5: 
                    self.colvalueindex=7
                elif  self.colvalueindex==7:
                    self.colvalueindex=5  
        
        if self.sheetname=='DCS2AI':         # 循环读取G6-AE30的值
                self.colvalueindex=self.colvalueindex+1  
                if self.colvalueindex>30: 
                    self.colvalueindex=6
                    
        return taglist   
    
    def SendToRedisHash(self):
        tagvaluelist=self.tag_from_excel()
        
        curtime=datetime.now()   # date & time
          
        pipe =conn.pipeline()
        for element in tagvaluelist:
            pipe.hmset(element['id'],{'desc':element['desc'],'value':element['value'],'ts':curtime})
        pipe.execute() 
        
        print(tagvaluelist[1]['desc'],tagvaluelist[1]['id'],conn.hmget(tagvaluelist[1]['id'],'value','ts'))
  
    def worker(self):
        self.SendToRedisHash()
        self.next_call = self.next_call + self.delay
        threading.Timer( self.next_call - time.time(), self.worker ).start()

if __name__ == "__main__": 
   
    rowbegindex=2
    colidindex=2
    coldescindex = 1
    colvalueindex=5  # F5列
    
    SensorU1AI = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowbegindex,colidindex,coldescindex,colvalueindex,u'DCS1AI') #F/H
    SensorU1AI.worker()
      
    SensorU1CO = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowbegindex,colidindex,coldescindex,colvalueindex,u'1CAL')  #F
    SensorU1CO.worker()
   
    colvalueindex=6  # G6列
    SensorU2AI = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowbegindex,colidindex,coldescindex,colvalueindex,u'DCS2AI') #G-AE
    SensorU2AI.worker()
    
    colvalueindex=5  # F5列
    SensorU2CO = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowbegindex,colidindex,coldescindex,colvalueindex,u'2CAL')  #F
    SensorU2CO.worker()
    
    SensorU3AI = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowbegindex,colidindex,coldescindex,colvalueindex,u'DCS3AI')  #F
    SensorU3AI.worker()
    
    SensorU3CO = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowbegindex,colidindex,coldescindex,colvalueindex,u'3CAL')  #F
    SensorU3CO.worker()
  
    SensorU4AI = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowbegindex,colidindex,coldescindex,colvalueindex,u'DCS4AI')  #F
    SensorU4AI.worker()
    
    SensorU4CO = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowbegindex,colidindex,coldescindex,colvalueindex,u'4CAL')  #F
    SensorU4CO.worker()
    
    SensorPLTCO = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowbegindex,colidindex,coldescindex,colvalueindex,u'PLANT') #F
    SensorPLTCO.worker()
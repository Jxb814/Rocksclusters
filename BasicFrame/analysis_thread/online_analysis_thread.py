# -*- coding: utf-8 -*-
"""
    Author:   Cheng Maohua
    Email:    cmh@seu.edu.cn
    License: MIT
"""
import threading
import time
 
class PeriodAnalysis():

    def __init__(self, delay, tasks):
        self.tasks = tasks
        self.delay = delay
        self.next_call = time.time()
  
    def setouttag(self):
        for task in self.tasks:
            task.setouttag()
    
    def worker(self):
        for task in self.tasks:
            task.run()
       
        self.next_call = self.next_call + self.delay
        threading.Timer(self.next_call - time.time(), self.worker).start()


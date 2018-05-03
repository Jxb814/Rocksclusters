'''
Created on 2018年4月27日
Read plant data from excel, put into redis
@author: user
'''
import xlrd
import redis

conn = redis.Redis('localhost')

class generalsheet():

    def __init__(self, file, rowindex, colnameindex, colsiindex, coldescindex, by_name):
        self.data = xlrd.open_workbook(file)
        self.rowindex = rowindex
        self.colnameindex = colnameindex
        self.colsiindex = colsiindex
        self.coldescindex = coldescindex

        self.table = self.data.sheet_by_name(by_name)
        self.nrows = self.table.nrows   # number of rows
        self.taglist = self.excel_tagdef_table()
        self.tagcount = len(self.taglist)

    def excel_tagdef_table(self):
        taglist = []
        for rownum in range(self.rowindex, self.nrows):
            tag = {'desc':u' ','name':u' ', 'si':u' ', 'value':'-1000'}
            tag['name'] = self.table.cell(rownum, self.colnameindex).value
            tag['desc'] = self.table.cell(rownum, self.coldescindex).value
            tag['si'] = self.table.cell(rownum, self.colsiindex).value

            taglist.append(tag)
            print(taglist[rownum - self.rowindex]['name'])

    def TagSnapshot(self):
        pipe = conn.pipeline()
        for element in self.taglist:
            pipe.hget(element['name'], 'value')
        tagvaluelist = pipe.excute()

        i = 0
        for i in range(self.tagcount):
            self.taglist[i]['value'] = tagvaluelist[i]
            i +=1

        return tagvaluelist
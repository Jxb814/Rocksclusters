'''
Created on 2018年4月27日
Read data from excel, put into redis
@author: user
'''
import xlrd
import redis
import scr.ThreadUpdateToRedisHash as db
from scr.TurbineCalculation import UnitHP

conn = redis.Redis('localhost')


class generalsheet():

    def __init__(self, datafile, sheet_name, uifile, by_name,
                 rowindex, uicolidindex, uicolsiindex, uicoldescindex, colvalueindex):
        self.usefuldata = xlrd.open_workbook(uifile)
        self.rowindex = rowindex
        self.uicolidindex = uicolidindex
        self.uicolsiindex = uicolsiindex
        self.uicoldescindex = uicoldescindex

        self.table = self.usefuldata.sheet_by_name(by_name)
        self.by_name = by_name
        self.nrows = self.table.nrows   # number of rows
        self.taglist = self.excel_tagdef()
        self.tagcount = len(self.taglist)
    # cs_tag_all 和 usefuldata 中id列号与si列号相反
        colidindex = uicolsiindex
        db.ThreadUpdateBegin(datafile, rowindex, colidindex,
                             colvalueindex, sheet_name)      # 开始循环读取数据

    def excel_tagdef(self):
        taglist = []
        for rownum in range(self.rowindex, self.nrows):
            tag = {'desc': u'', 'id': u'', 'si': u'', 'value': '-1000',
                   'x': 20, 'y': 20, 'fig': 0, 'tab': 0}
            tag['id'] = self.table.cell(rownum, self.uicolidindex).value
            tag['desc'] = self.table.cell(rownum, self.uicoldescindex).value
            tag['si'] = self.table.cell(rownum, self.uicolsiindex).value

            tag['x'] = self.table.cell(rownum, 8).value
            tag['y'] = self.table.cell(rownum, 9).value

            tag['fig'] = self.table.cell(rownum, 10).value
            tag['tab'] = self.table.cell(rownum, 11).value

            taglist.append(tag)

            print(taglist[rownum - self.rowindex]['id'])

        return taglist

    def GetTagDefFromExcel(self):
        return self.taglist

    def TagSnapshot(self):
        '''
        get data from redis
        '''
        pipe = conn.pipeline()
        for element in self.taglist:
            print(element)
            pipe.hget(element['id'], 'value')
        tagvaluelist = pipe.execute()    # ordered list 只有value值 string类型)

        i = 0
        for i in range(self.tagcount):
            self.taglist[i]['value'] = tagvaluelist[i]
            i += 1                     # taglist中 id与value对应

        self.calculation()             # 计算后再读一遍

        pipe = conn.pipeline()
        for element in self.taglist:
            pipe.hget(element['id'], 'value')
        tagvaluelist = pipe.execute()    # ordered list 只有value值

        i = 0
        for i in range(self.tagcount):
            self.taglist[i]['value'] = tagvaluelist[i]
            i += 1                     # taglist中 id与value对应

        flttagvaluelist = list()
        for element in tagvaluelist:
            if element is not None:
                flttagvaluelist.append(float(element))
            else:
                flttagvaluelist.append(element)

        return flttagvaluelist

    def desc_valueMatch(self):
        tagdict = {}
        for i in range(self.tagcount):
            if self.taglist[i]['value'] is not None:
                tagdict[self.taglist[i]['desc']] = float(self.taglist[i]['value'])
        return tagdict

    def calculation(self):
        if self.by_name == u'rh_draw':
            HP = UnitHP(self)
            self.taglist = HP.HeatRateCaculation()
        else:
            pass
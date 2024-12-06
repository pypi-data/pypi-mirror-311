# python -m unittest wutils.py
'''
20240411 新增trade_date处理日期段头尾的相关函数
20240412 bizd只保存放假日和调休日就行
每年交易日是243天 242.8 2003-2024的统计结果
20241115 bizd不变 另造一个非weekend的holiday文件 以辅助生成bizd
'''

import unittest
import datetime
from pathlib import Path

class trade_date(object):
    '''
    返回日期 int or [int]
    '''
    # date_to_seq
    # seq_to_date
    ds = {}
    sd = {}


    sysdir = Path(__file__).parent
    date_file = f"{sysdir}/bizd.txt"

    with open(date_file) as f:
        for i, j in enumerate(f.readlines()):
            ds[int(j.strip())] = int(i)
        sd = {v: k for k, v in ds.items()}

    dts = set(ds.keys())

    @classmethod
    def isbizd(cls, dt):
        dt = int(dt)
        if dt in cls.dts:
            return True
        return False

    @classmethod
    def today(cls):
        return int(datetime.datetime.now().strftime("%Y%m%d"))

    @classmethod
    def getbizds(cls, bd, ed):
        '''
        两天之间的所有交易日
        '''
        bd = int(bd)
        ed = int(ed)
        re = []
        if cls.isbizd(bd):
            re.append(bd)
        tmpd = cls.nextbizd(bd)
        while tmpd <= ed:
            re.append(tmpd)
            tmpd = cls.nextbizd(tmpd)
        return re

    @classmethod
    def getbizdcount(cls, bd, ed):
        '''
        两天之间的交易日个数
        '''
        bd = int(bd)
        ed = int(ed)
        re = 0
        if cls.isbizd(bd):
            re = re + 1
        bd = cls.nextbizd(bd)
        if cls.isbizd(ed):
            re = re + 1
        ed = cls.prebizd(ed)
        return re + cls.ds[ed] - cls.ds[bd] + 1

    @classmethod
    def getbizdsfrom(cls, bd, num):
        '''
        从特定日开始往后数连续多少个交易日
        '''
        bd = int(bd)
        re = []
        if num < 1:
            return re
        tmpd = 0
        if cls.isbizd(bd):
            tmpd = bd
        else:
            tmpd = cls.nextbizd(bd)
        while num > 0:
            re.append(tmpd)
            tmpd = cls.nextbizd(tmpd)
            num = num - 1
        return re

    @classmethod
    def getbizdsto(cls, dt, num):
        '''
        从特定日开始往前数连续多少个交易日
        '''
        dt = int(dt)
        re = []
        if num < 1:
            return re
        tmpd = 0
        if cls.isbizd(dt):
            tmpd = dt
        else:
            tmpd = cls.prebizd(dt)
        while num > 0:
            re.append(tmpd)
            tmpd = cls.prebizd(tmpd)
            num = num - 1
        re.reverse()
        return re

    @classmethod
    def prebizd(cls, dt, num=1):
        '''
        这天之前的第一个交易日 或第N个交易日
        '''
        dt = int(dt)
        if num != 1:
            return cls.getbizdsto(dt, num + 1)[0]
        if dt < 20000000 or dt > 21000000:
            return 0
        if dt in cls.dts:
            if cls.ds[dt] - 1 in cls.sd.keys():
                return cls.sd[cls.ds[dt] - 1]
        dt -= 1
        while dt > 20000000:
            if dt in cls.dts:
                return dt
            dt -= 1
        return 0

    @classmethod
    def nextbizd(cls, dt, num=1):
        '''
        这天之后的第一个交易日 或第N个交易日
        '''
        dt = int(dt)
        if num != 1:
            return cls.getbizdsfrom(dt, num + 1)[num]
        if dt < 20000000 or dt > 21000000:
            return 0
        # if dt in cls.ds.keys(): # 用__contains__ 和get() 都更慢
        if dt in cls.dts:  # 用set快些
            if cls.ds[dt] + 1 in cls.sd.keys():
                return cls.sd[cls.ds[dt] + 1]
        dt += 1
        while dt < 21000000:
            if dt in cls.dts:
                return dt
            dt += 1
        return 0

    @classmethod
    def calendar_diff(cls, bd, ed):
        '''
        两天之间差多少天
        '''
        bd = str(bd)
        ed = str(ed)
        bdd = datetime.datetime(int(bd[0:4]), int(bd[4:6]), int(bd[6:]))
        edd = datetime.datetime(int(ed[0:4]), int(ed[4:6]), int(ed[6:]))
        return (edd - bdd).days

    @classmethod
    def bizd_diff(cls, bd, ed):
        '''
        两天之间差多少交易日
        '''
        if bd > ed:
            bd, ed = ed, bd
        while not trade_date.isbizd(bd):
            bd = trade_date.prebizd(bd)
        while not trade_date.isbizd(ed):
            ed = trade_date.prebizd(ed)
        diff = 0
        while bd < ed:
            bd = trade_date.nextbizd(bd)
            diff += 1
        return diff

    @classmethod
    def week_day(cls,dt):
        '''
        返回当前是周几 范围是1-7
        '''
        dt = str(dt)
        dt = datetime.date(int(dt[0:4]), int(dt[4:6]), int(dt[6:8]))
        return dt.weekday() + 1

    @classmethod
    def get_calendar_days(cls,bd,ed):
        '''
        返回日历日日期范围
        '''
        ret=[bd,ed]
        bd = str(bd)
        ed = str(ed)
        bdd = datetime.datetime(int(bd[0:4]), int(bd[4:6]), int(bd[6:]))
        edd = datetime.datetime(int(ed[0:4]), int(ed[4:6]), int(ed[6:]))
        while bdd < edd:
            bdd = bdd + datetime.timedelta(days=1)
            ret.append(bdd.strftime("%Y%m%d"))
        ret=sorted([int(x) for x in ret])
        return sorted(set(ret))
        
    @classmethod
    def premonth(cls,dt, num):
        """
        找之前的第几个月的第一天 20200104 ,2 ->20191101
        """
        dt = str(dt)
        year = int(str(dt)[0:4])
        month = int(str(dt)[4:6])

        lend = int((num - month + 12) / 12)
        year = year - lend
        month = (month - num) % 12
        month = 12 if month == 0 else month

        return year * 10000 + month * 100 + 1


    @classmethod
    def gotobizd(cls,dt, reverse=False):
        """
        如果当前日期是交易日则返回当前日期
        否则返回大于当前日期的第一个交易日
        reverse小于当前日期的第一个交易日
        """
        if trade_date.isbizd(dt):
            return dt
        elif reverse:
            return trade_date.prebizd(dt)
        else:
            return trade_date.nextbizd(dt)
    
    @classmethod
    def bizdhead(cls,bd,ed,week=False,month=False,holiday=True,tail=False):
        """
        返回起止日期中间的各种周期的第一个交易日
        默认是每个非交易日的下一个交易日
        week=True 返回每周的第一个交易日 这个在周三只休一天时候与默认的区别
        month=True 返回每月的第一个交易日
        tail=True 返回每个周期的最后一个交易日
        """
        bd=int(bd)
        ed=int(ed)
        ret=[]
        if bd>=ed:
            return ret
        by=int(bd/10000)
        ey=int(ed/10000)
        while(by<=ey):
            ret.extend(cls.bizdheadyear(by,week=week,month=month,holiday=holiday,tail=tail))
            by=by+1
        ret=[x for x in ret if x>=bd and x<=ed]
        return sorted(set(ret))
    @classmethod
    def bizdheadyear(cls,year,week=False,month=False,holiday=True,tail=False):
        """
        返回一年中的各种周期的第一个交易日
        默认是每个非交易日的下一个交易日
        week=True 返回每周的第一个交易日 这个在周三只休一天时候与默认的区别
        month=True 返回每月的第一个交易日
        tail=True 返回每个周期的最后一个交易日
        """
        year=int(year)
        if month:
            week=False
        if week:
            holiday=False
        ret=[]
        if month:
            for i in range(12):
                if tail:
                    dt=year*10000+(i+1)*100+32
                    ret.append(cls.gotobizd(dt,reverse=True))
                else:
                    dt=year*10000+(i+1)*100
                    ret.append(cls.gotobizd(dt)) 
        elif holiday or week:
            bd=(year-1)*10000+1200+1
            ed=(year+1)*10000+200+1
            for day in cls.get_calendar_days(bd,ed):
                if cls.isbizd(day):
                    continue
                elif holiday or (week and cls.week_day(day)>=6):
                    ret.append(cls.gotobizd(day,reverse=tail))
            ret=[x for x in ret if int(x/10000)==year]
        return sorted(set(ret))

class TestDict(unittest.TestCase):
    def test_trade_date(self):
        a = trade_date
        self.assertEqual(a.nextbizd(0), 0)
        self.assertEqual(a.nextbizd(20180100), 20180102)
        self.assertEqual(a.nextbizd(20180813), 20180814)
        self.assertEqual(a.prebizd(0), 0)
        self.assertEqual(a.prebizd(20180100), 20171229)
        self.assertEqual(a.prebizd(20180813), 20180810)
        self.assertEqual(a.isbizd(20180100), False)
        self.assertEqual(a.isbizd(20180813), True)
        self.assertEqual(a.getbizdcount(20180102, 20180105), 4)
        self.assertEqual(
            a.getbizds(20180101, 20180105), [20180102, 20180103, 20180104, 20180105]
        )
        self.assertEqual(
            a.getbizds(20180102, 20180105), [20180102, 20180103, 20180104, 20180105]
        )
        self.assertEqual(
            a.getbizdsto(20180105, 4), [20180102, 20180103, 20180104, 20180105]
        )
        self.assertEqual(
            a.getbizdsfrom(20180102, 4), [20180102, 20180103, 20180104, 20180105]
        )
        self.assertEqual(a.getbizds(20180100, 20180101), [])



if __name__ == "__main__":
    unittest.main()

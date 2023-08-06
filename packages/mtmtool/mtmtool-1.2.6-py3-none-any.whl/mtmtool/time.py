import time
import datetime, calendar


class sTime:
    def __init__(self, srctime=None):
        self.datetime = srctime

    def __call__(self, srctime):
        self.datetime = srctime
        return self

    def fromstr(self, timestr, format="%Y-%m-%d"):
        self.datetime = datetime.datetime.strptime(timestr, format)
        return self

    def tostr(self, format="%Y-%m-%d"):
        return self.datetime.strftime(format)

    def last_month(self, objday=1):
        self.datetime = (self.datetime.replace(day=1) - datetime.timedelta(days=1)).replace(day=objday)
        return self

    def next_month(self, objday=1):
        week, days_num = calendar.monthrange(self.datetime.year, self.datetime.month)
        self.datetime = (self.datetime.replace(day=days_num) + datetime.timedelta(days=1)).replace(day=objday)
        return self

    def next_day(self):
        self.datetime = self.datetime + datetime.timedelta(days=1)
        return self

    def last_day(self):
        self.datetime = self.datetime - datetime.timedelta(days=1)
        return self


def timestamp2timestr(timeStamp, format="%Y-%m-%d %H:%M:%S", isMicroSecond=True, isUtc=False):
    time_function = time.gmtime if isUtc else time.localtime
    return time.strftime(format, time_function(timeStamp / (1000 if isMicroSecond else 1)))


def timestr2timestamp(timestr, format="%Y-%m-%d %H:%M:%S", isMicroSecond=True):
    timeArray = time.strptime(timestr, format)
    return int(time.mktime(timeArray)) * (1000 if isMicroSecond else 1)


st = sTime()
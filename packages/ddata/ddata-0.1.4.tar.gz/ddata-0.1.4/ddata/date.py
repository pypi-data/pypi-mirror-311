# -*- coding: utf-8 -*-
import datetime
import time


class DateUtil:
    def __init__(self):
        pass

    @staticmethod
    def date_2_hyphen_date(date):
        """
        转成中划线日期
        :param date:
        :return:
        """
        res = date[0: 4] + '-' + date[4: 6] + '-'+date[6: 8]
        return res

    # 计算时间函数
    @staticmethod
    def timer(func):
        def wrapper(*args, **kw):
            start_time = time.time()
            print(DateUtil.now(), '[%s] start to run program.........' % func.__name__)
            ret = func(*args, **kw)
            end_time = time.time()
            # print(DateUtil.now(), "程序运行结束，共使用了{} 分钟".format(round((end_time - start_time) / 60, 2)))
            print(DateUtil.now(), ' [%s] program is end, cost time: %.2f minute.........' % (func.__name__, round((end_time - start_time) / 60, 2)))
            return ret

        return wrapper

    @staticmethod
    def get_today():
        formatter = "%Y%m%d"
        today_val = datetime.date.today()
        today = today_val.strftime(formatter)
        return today

    @staticmethod
    def today(formatter):
        """
        获取今天的日期的值
        :param formatter: 日期的格式，默认为%Y%m%d，20170101
        :return:
        """
        today_val = datetime.date.today()
        if formatter is None or formatter == "":
            formatter = "%Y%m%d"
        today = today_val.strftime(formatter)
        return today

    @staticmethod
    def yesterday(formatter=None):
        today_val = datetime.date.today()
        timedelta = datetime.timedelta(days=1)
        yesterday_val = today_val - timedelta
        if formatter is None or formatter == "":
            formatter = "%Y%m%d"
        yesterday = yesterday_val.strftime(formatter)
        return yesterday

    @staticmethod
    def now():
        """
        获取当前的时间
        :param formatter: 时间的格式，比如%Y-%m-%d %H:%M:%S
        :return:
        """
        formatter = "%Y-%m-%d %H:%M:%S.%f"
        return datetime.datetime.now().strftime(formatter)[:-3]

    @staticmethod
    def formatter_now(formatter):
        """
        获取当前的时间
        :param formatter: 时间的格式，比如%Y-%m-%d %H:%M:%S
        :return:
        """
        if formatter is None or formatter == "":
            formatter = "%Y-%m-%d %H:%M:%S"

        return time.strftime(formatter, time.localtime())

    @staticmethod
    def n_day_ago(date, n):
        """
        获取n天之前的日期
        :param date:
        :param n:
        :return:
        """
        if date is None or date == "":
            date = datetime.date.today().strftime("%Y%m%d")

        if n is None or n == "":
            n = 1

        one_day_ago = datetime.datetime.strptime(date, "%Y%m%d") + datetime.timedelta(
            days=-n
        )
        return one_day_ago.strftime("%Y%m%d")

    @staticmethod
    def n_day_later(date, n):
        """
        获取n天之后的日期
        :param date:
        :param n:
        :return:
        """
        if date is None or date == "":
            date = datetime.date.today().strftime("%Y%m%d")

        if n is None or n == "":
            n = 1

        one_day_ago = datetime.datetime.strptime(date, "%Y%m%d") + datetime.timedelta(
            days=n
        )
        return one_day_ago.strftime("%Y%m%d")

    @staticmethod
    def almost_n_month_ago(date, n):
        """
        近似获取n月之前的日期,
        :param date:
        :param n:
        :return:
        """
        if date is None or date == "":
            date = datetime.date.today().strftime("%Y%m")

        if n is None or n == "":
            n = 1

        date = date + "01"
        one_day_ago = datetime.datetime.strptime(date, "%Y%m%d") + datetime.timedelta(
            days=-n * 28
        )
        return one_day_ago.strftime("%Y%m")

    @staticmethod
    def timestamp_2_yyyy_mm(timestamp):
        x = time.localtime(timestamp)
        return time.strftime("%Y%m", x)

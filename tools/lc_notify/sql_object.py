"""sql object for each table"""
import settings
from datetime import datetime
from dao import Dao
from loghandle import logger

class UserDailyInfoRecord:
    def __int__(self):
        self.user = ''
        self.total_solve = 0
        self.code_submit = 0
        self.problem_submit = 0
        self.rating_score = 0
        self.continue_days = 0
        self.new_solve = 0
        self.lazy_days = 0
        self.total_days = 0
        self.date_time = ''
        
    def as_dict(self):
        return {
            'user' : self.user,
            'total_solve': self.total_solve,
            'code_submit': self.code_submit,
            'problem_submit': self.problem_submit,
            'rating_score': self.rating_score,
            'continue_days': self.continue_days,
            'new_solve': self.new_solve,
            'lazy_days': self.lazy_days,
            'total_days': self.total_days,
            'date_time': self.date_time
        }


class DaoDailyInfo(Dao):
    FIELDS = ['user', 'total_solve', 'code_submit',
              'problem_submit', 'rating_score', 'continue_days',
              'new_solve', 'lazy_days', 'total_days','date_time']
    TABLE = 'user_lc_daily_info'
    
    def __init__(self):
        pass
    
    def search_user_recent_info(self, user):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.FIELDS) + \
            " from " + self.TABLE + \
            " where user = '%s' order by date_time desc limit 1" % user
        datas = self._query(sql)
        if not datas:
            return None
        if len(datas) > 0:
            return datas[0]
        return None
    
    def load_all_user_daily_info_by_day(self, date):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.FIELDS) + \
            " from " + self.TABLE + " where date_time = '%s'" % date
        datas = self._query(sql)
        
        if not datas:
            return None
        resp = {}
        for data in datas:
            item = UserDailyInfoRecord()
            item.user = data[0]
            item.total_solve = data[1]
            item.code_submit = data[2]
            item.problem_submit = data[3]
            item.rating_score = data[4]
            item.continue_days = data[5]
            item.new_solve = data[6]
            item.lazy_days = data[7]
            item.total_days = data[8]
            item.date_time = data[9]
            resp[item.user] = item
        return resp
    
    def search_user_recent_info(self, user):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.FIELDS) + \
            " from " + self.TABLE + \
            " where user = '%s' order by date_time desc limit 1" % user
        datas = self._query(sql)
        if not datas:
            return None
        if len(datas) > 0:
            data = datas[0]
            item = UserDailyInfoRecord()
            item.user = data[0]
            item.total_solve = data[1]
            item.code_submit = data[2]
            item.problem_submit = data[3]
            item.rating_score = data[4]
            item.continue_days = data[5]
            item.new_solve = data[6]
            item.lazy_days = data[7]
            item.total_days = data[8]
            item.date_time = data[9]
            return item
        return None
    
    def serach_single_user_daily_info(self, user, date):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.FIELDS) + \
            " from " + self.TABLE + \
            " where user = '%s' and date_time = '%s'" % (user, date)
        datas = self._query(sql)
        if not datas:
            return None
        if len(datas) > 0:
            data = datas[0]
            item = UserDailyInfoRecord()
            item.user = data[0]
            item.total_solve = data[1]
            item.code_submit = data[2]
            item.problem_submit = data[3]
            item.rating_score = data[4]
            item.continue_days = data[5]
            item.new_solve = data[6]
            item.lazy_days = data[7]
            item.total_days = data[8]
            item.date_time = data[9]
            return item
        return None
    
    def reset_single_user_lazy_days(self, user):
        if not self._connect_mysql():
            return False
        sql = "update " + self.TABLE + " set \
            lazy_days=0 where user = '%s'" % user
        return self._update(sql)
    
    def update_single_user_daily_info(self, date, item):
        if not self._connect_mysql():
            return False
        sql = "update " + self.TABLE + " set \
            total_solve=%s, code_submit=%s, problem_submit=%s, rating_score=%s, \
            continue_days=%s, new_solve=%s, lazy_days=%s, total_days=%s where user = '%s' and  date_time ='%s'" % (data[1],
                                                                                                    data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[0], date)
        return self._update(sql)
    
    def add_single_user_daily_info(self, date: datetime, item: UserDailyInfoRecord):
        if not self._connect_mysql():
            return False
        presql = "insert into " + self.TABLE
        presql += " (" + ",".join(self.FIELDS) + ")"
        sql = presql + "values ('%s',%s, %s, %s, %s, %s, %s, %s, %s, '%s')" % \
            (item.user, item.total_solve, item.code_submit, item.problem_submit, item.rating_score,
                item.continue_days, item.new_solve, item.lazy_days,item.total_days, date)
        print(sql)
        return self._add(sql)
    
obj = DaoDailyInfo()
item = obj.serach_single_user_daily_info('smilecode-2', '2023-02-20')
item.user = 'smilecode-22'
obj.add_single_user_daily_info(datetime.today(), item)

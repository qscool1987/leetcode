"""sql object for each table"""
from dao.dao import Dao
import sys
sys.path.append('..')


class UserDailyInfoRecord:
    def __init__(self):
        self.user = ''
        self.total_solve = 0
        self.code_submit = 0
        self.problem_submit = 0
        self.rating_score = 0
        self.continue_days = 1
        self.new_solve = 0
        self.lazy_days = 0
        self.total_days = 1
        self.date_time = ''
        self.hard_num = 0
        self.mid_num = 0
        self.easy_num = 0
        self.hard_total = 0
        self.mid_total = 0
        self.easy_total = 0

    def as_dict(self):
        return {
            'user': self.user,
            'total_solve': self.total_solve,
            'code_submit': self.code_submit,
            'problem_submit': self.problem_submit,
            'rating_score': self.rating_score,
            'continue_days': self.continue_days,
            'new_solve': self.new_solve,
            'lazy_days': self.lazy_days,
            'total_days': self.total_days,
            'date_time': str(self.date_time),
            'hard_num': self.hard_num,
            'mid_num': self.mid_num,
            'easy_num': self.easy_num,
            'hard_total': self.hard_total,
            'mid_total': self.mid_total,
            'easy_total': self.easy_total
        }


class DaoDailyInfo(Dao):
    FIELDS = ['user', 'total_solve', 'code_submit',
              'problem_submit', 'rating_score', 'continue_days',
              'new_solve', 'lazy_days', 'total_days', 'hard_num',
              'mid_num', 'easy_num', 'hard_total', 'mid_total', 'easy_total', 'date_time']
    TABLE = 'user_lc_daily_info'

    def __init__(self):
        pass

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
            item.hard_num = data[9]
            item.mid_num = data[10]
            item.easy_num = data[11]
            item.hard_total = data[12]
            item.mid_total = data[13]
            item.easy_total = data[14]
            item.date_time = data[15]
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
            item.hard_num = data[9]
            item.mid_num = data[10]
            item.easy_num = data[11]
            item.hard_total = data[12]
            item.mid_total = data[13]
            item.easy_total = data[14]
            item.date_time = data[15]
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
            item.hard_num = data[9]
            item.mid_num = data[10]
            item.easy_num = data[11]
            item.hard_total = data[12]
            item.mid_total = data[13]
            item.easy_total = data[14]
            item.date_time = data[15]
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
            continue_days=%s, new_solve=%s, lazy_days=%s, total_days=%s, hard_num=%s, mid_num=%s, easy_num=%s, hard_total=%s, mid_total=%s, easy_total=%s where user = '%s' and \
            date_time ='%s'" % (item.total_solve, item.code_submit, item.problem_submit,
                                item.rating_score, item.continue_days, item.new_solve, item.lazy_days, item.total_days,
                                item.hard_num, item.mid_num, item.easy_num, item.hard_total, item.mid_total, item.easy_total, item.user, date)
        return self._update(sql)

    def add_single_user_daily_info(self, item: UserDailyInfoRecord):
        if not self._connect_mysql():
            return False
        presql = "insert into " + self.TABLE
        presql += " (" + ",".join(self.FIELDS) + ")"
        sql = presql + "values ('%s',%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,'%s')" % \
            (item.user, item.total_solve, item.code_submit, item.problem_submit, item.rating_score,
                item.continue_days, item.new_solve, item.lazy_days, item.total_days, item.hard_num, item.mid_num, item.easy_num, item.hard_total, item.mid_total, item.easy_total, item.date_time)
        return self._add(sql)

    def count_user_total_days(self, user):
        if not self._connect_mysql():
            return False
        sql = "select count(*) from " + self.TABLE + \
            " where user = '%s' and new_solve > 0 and date_time < '2023-02-21'" % user
        data = self._query(sql)
        return data[0][0]

    def update_user_total_days(self, user, days):
        if not self._connect_mysql():
            return False
        sql = "update " + self.TABLE + " set total_days = %s " \
            "where user = '%s'" % (days, user)
        return self._update(sql)

    def update_user_problem_number(self, user, num, date_time):
        if not self._connect_mysql():
            return False
        sql = "update user_lc_daily_info set total_solve=%s where user='%s' \
               and date_time='%s'" % (num, user, date_time)
        return self._update(sql)
    
    def load_all_user_daily_infos(self):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.FIELDS) + \
            " from " + self.TABLE
        datas = self._query(sql)
        if not datas:
            return None
        resp = []
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
            item.hard_num = data[9]
            item.mid_num = data[10]
            item.easy_num = data[11]
            item.hard_total = data[12]
            item.mid_total = data[13]
            item.easy_total = data[14]
            item.date_time = data[15]
            resp.append(item)
        return resp

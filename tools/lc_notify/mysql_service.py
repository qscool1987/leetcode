# coding=utf-8
import pymysql
from loghandle import logger
import datetime
import settings
import sys

problem_types = ["算法编程", "Java", "C++", "操作系统",
                 "计算机网络", "mysql", "redis", "mq", "并发编程", "分布式系统"]


class MysqlService(object):
    """
    table list
    """
    ACCOUNT_INFO_TABLE = 'account_info'
    USER_LC_DAILY_INFO_TABLE = 'user_lc_daily_info'
    FEEDBACK_INFO_TABLE = 'feedback_info'
    USER_ATGERT_INFO_TABLE = 'user_target_info'
    RAND_PROBLEM_INFO_TABLE = 'rand_problem_info'
    INTERVIEW_PROBLEM_INFO_TABLE = 'interview_problem_info'
    USER_LC_DAILY_INFO_FIELDS = ['user', 'total_solve', 'code_submit',
                                 'problem_submit', 'rating_score', 'continue_days',
                                 'new_solve', 'lazy_days', 'date_time']
    ACCOUNT_INFO_FIELDS = ['user', 'git_account',
                           'medal', 'award', 'email', 'date_time', 'coins']
    FEEDBACK_INFO_FIELDS = ['content', 'status', 'answer', 'date_time']
    USER_ATGERT_INFO_FIELDS = ['user', 'target_type', 'target_value', 'opponent',
                               'status', 'create_date', 'dead_line', 'level']
    RAND_PROBLEM_INFO_FIELDS = [
        'user', 'lc_number', 'status', 'coins', 'create_time']
    INTERVIEW_PROBLEM_INFO_FIELDS = [
        'content', 'answer', 'type', 'company', 'jd']

    def __init__(self):
        self.port = 3306
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'qscool'
        self.db = 'leetcode'
        self.conn = None
        self.cur = None

    def _connect_mysql(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                db=self.db,
                port=self.port
            )
            self.cur = self.conn.cursor()
            return True
        except Exception as e:
            logger.error(e)
            self.conn = None
            self.cur = None
            return False

    def add_single_user_daily_info(self, date, data):
        if not self._connect_mysql():
            return False
        presql = "insert into " + self.USER_LC_DAILY_INFO_TABLE
        presql += " (" + ",".join(self.USER_LC_DAILY_INFO_FIELDS) + ")"
        user = data[0]
        total = int(data[1])
        code_submit = int(data[2])
        problem_submit = int(data[3])
        score = int(data[4])
        days = int(data[5])
        new_solve = int(data[6])
        lazy_days = int(data[7])
        sql = presql + "values ('%s',%s, %s, %s, %s, %s, %s, %s, '%s')" % \
            (user, total, code_submit, problem_submit, score,
                days, new_solve, lazy_days, date)
        return self._add(sql)

    def update_single_user_daily_info(self, date, data):
        if not self._connect_mysql():
            return False
        sql = "update " + self.USER_LC_DAILY_INFO_TABLE + " set \
            total_solve=%s, code_submit=%s, problem_submit=%s, rating_score=%s, \
            continue_days=%s, new_solve=%s, lazy_days=%s where user = '%s' and  date_time ='%s'" % (data[1],
                                                                                                    data[2], data[3], data[4], data[5], data[6], data[7], data[0], date)
        return self._update(sql)
    def reset_single_user_lazy_days(self, user):
        if not self._connect_mysql():
            return False
        sql = "update " + self.USER_LC_DAILY_INFO_TABLE + " set \
            lazy_days=0 where user = '%s'" % user
        return self._update(sql)

    def serach_single_user_daily_info(self, user, date):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.USER_LC_DAILY_INFO_FIELDS) + \
            " from " + self.USER_LC_DAILY_INFO_TABLE + \
            " where user = '%s' and date_time = '%s'" % (user, date)
        datas = self._query(sql)
        if not datas:
            return None
        if len(datas) > 0:
            return datas[0]
        return None

    def search_user_recent_info(self, user):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.USER_LC_DAILY_INFO_FIELDS) + \
            " from " + self.USER_LC_DAILY_INFO_TABLE + \
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
        sql = "select " + ",".join(self.USER_LC_DAILY_INFO_FIELDS) + \
            " from " + self.USER_LC_DAILY_INFO_TABLE + " where date_time = '%s'" % date
        datas = self._query(sql)
        if not datas:
            return None
        res = {}
        for data in datas:
            res[data[0]] = data
        return res

    def load_all_user_daily_infos(self):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.USER_LC_DAILY_INFO_FIELDS) + \
            " from " + self.USER_LC_DAILY_INFO_TABLE
        return self._query(sql)

    def update_user_medal(self, user, medal):
        if not self._connect_mysql():
            return False
        sql = "update " + self.ACCOUNT_INFO_TABLE + " set medal = %s \
            where user = '%s'" % (medal, user)
        return self._update(sql)

    def update_user_email(self, user, email):
        if not self._connect_mysql():
            return False
        sql = "update " + self.ACCOUNT_INFO_TABLE + " set email = '%s' \
            where user = '%s'" % (email, user)
        return self._update(sql)

    def update_user_git_account(self, user, git_account):
        if not self._connect_mysql():
            return False
        sql = "update " + self.ACCOUNT_INFO_TABLE + " set git_account = '%s' \
            where user = '%s'" % (git_account, user)
        return self._update(sql)

    def update_user_award(self, user, val):
        if not self._connect_mysql():
            return False
        sql = "update " + self.ACCOUNT_INFO_TABLE + " set award = %s \
            where user = '%s'" % (val, user)
        return self._update(sql)

    def update_account_status(self, user, status):
        if not self._connect_mysql():
            return False
        sql = "update " + self.ACCOUNT_INFO_TABLE + " set status = %s \
            where user = '%s'" % (status, user)
        return self._update(sql)

    def add_account_info(self, user, git_user='', email='', award=0, medal=0, coins=100):
        if not self._connect_mysql():
            return False
        td = datetime.date.today()
        td = str(td)
        sql = "insert into " + self.ACCOUNT_INFO_TABLE + " (" + \
            ",".join(self.ACCOUNT_INFO_FIELDS) + ") values('%s', '%s', %s, %s, '%s', '%s', %s)" \
            % (user, git_user, medal, award, email, td, coins)
        return self._add(sql)

    def search_account(self, user):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.ACCOUNT_INFO_FIELDS) + " from " + \
            self.ACCOUNT_INFO_TABLE + " where user = '%s'" % user
        datas = self._query(sql)
        if not datas:
            return None
        if len(datas) > 0:
            return datas[0]
        return None

    def load_all_email_users(self):
        if not self._connect_mysql():
            return False
        sql = "select user, email from " + self.ACCOUNT_INFO_TABLE + \
            " where email != '' and status = 0"
        return self._query(sql)

    def load_all_account_infos(self):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.ACCOUNT_INFO_FIELDS) + \
            " from " + self.ACCOUNT_INFO_TABLE + " where status < 1"
        datas = self._query(sql)
        if not datas:
            return None
        user_to_git = {}
        user_medal = {}
        user_award = {}
        user_email = {}
        for data in datas:
            if data[1] != '':
                user_to_git[data[0]] = data[1]
            user_medal[data[0]] = data[2]
            user_award[data[0]] = data[3]
            if data[4] != '':
                user_email[data[0]] = data[4]
        return user_to_git, user_medal, user_award, user_email

    def load_all_accounts(self):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.ACCOUNT_INFO_FIELDS) + \
            " from " + self.ACCOUNT_INFO_TABLE
        return self._query(sql)

    def load_all_account_coins(self):
        if not self._connect_mysql():
            return False
        sql = "select user, coins from " + self.ACCOUNT_INFO_TABLE
        datas = self._query(sql)
        if not datas:
            return None
        user_coins = {}
        for data in datas:
            user_coins[data[0]] = data[1]
        return user_coins

    def update_user_coins(self, user, coins):
        if not self._connect_mysql():
            return False
        sql = "update " + self.ACCOUNT_INFO_TABLE + \
            " set coins = %s where user = '%s'" % (coins, user)
        return self._update(sql)

    def search_user_coins(self, user):
        if not self._connect_mysql():
            return False
        sql = "select coins from " + self.ACCOUNT_INFO_TABLE + " where user = '%s'" % user
        data = self._query(sql)
        if not data:
            return None
        if len(data) > 0:
            return data[0][0]
        return None

    def add_feedback_info(self, date, content):
        if not self._connect_mysql():
            return False
        sql = "insert into " + self.FEEDBACK_INFO_TABLE + " (" + \
            ",".join(self.FEEDBACK_INFO_FIELDS) + ") values('%s', %s, '%s', '%s')" \
            % (content, 1, '', date)
        return self._add(sql)

    def update_feedback_status(self, id, status):
        if not self._connect_mysql():
            return False
        sql = "update " + self.FEEDBACK_INFO_TABLE + \
            " set status = %s where id = %d" % (status, id)
        return self._update(sql)

    def update_feedback_answer(self, id, answer):
        if not self._connect_mysql():
            return False
        sql = "update " + self.FEEDBACK_INFO_TABLE + \
            " set answer = '%s' where id = %d" % (answer, id)
        return self._update(sql)

    def load_feedback_info(self, pn, rn):
        if not self._connect_mysql():
            return False
        sql = "select * from " + self.FEEDBACK_INFO_TABLE + \
            " order by date_time desc limit %s, %s" % (pn, rn)
        return self._query(sql)

    def update_user_problem_number(self, user, num, date_time):
        if not self._connect_mysql():
            return False
        sql = "update user_lc_daily_info set total_solve=%s where user='%s' \
               and date_time='%s'" % (num, user, date_time)
        return self._update(sql)

    def add_user_target(self, info):
        if not self._connect_mysql():
            return False
        sql = "insert into " + self.USER_ATGERT_INFO_TABLE + " (" + \
            ",".join(self.USER_ATGERT_INFO_FIELDS) + ") values('%s', %s, %s, '%s', %s, '%s', '%s', '%s')" \
            % (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7])
        return self._add(sql)

    def load_all_unfinished_target_info(self):
        if not self._connect_mysql():
            return False
        sql = "select * " + \
            " from " + self.USER_ATGERT_INFO_TABLE + " where status = 1"
        return self._query(sql)

    def load_all_unfinished_target_info2(self):
        if not self._connect_mysql():
            return False
        sql = "select * " + \
            " from " + self.USER_ATGERT_INFO_TABLE + \
            " where target_type = 2 and status = 1"
        return self._query(sql)

    def load_single_user_unfinished_target_info(self, user):
        if not self._connect_mysql():
            return False
        sql = "select * " + \
            " from " + self.USER_ATGERT_INFO_TABLE + \
            " where status = 1 and user = '%s'" % user
        return self._query(sql)

    def update_user_target_status(self, id, status):
        if not self._connect_mysql():
            return False
        sql = "update " + self.USER_ATGERT_INFO_TABLE + \
            " set status = %d where id = %d" % (status, id)
        return self._update(sql)

    def update_user_target_level(self, id, level):
        if not self._connect_mysql():
            return False
        sql = "update " + self.USER_ATGERT_INFO_TABLE + \
            " set level = %d where id = %d" % (level, id)
        return self._update(sql)

    def get_user_target_info(self, pn, rn):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.USER_ATGERT_INFO_FIELDS) + \
            " from " + self.USER_ATGERT_INFO_TABLE + \
            " order by create_date desc limit %s, %s" % (pn, rn)
        return self._query(sql)

    def add_rand_problem_record(self, user, lc_number, coins, status, date):
        if not self._connect_mysql():
            return False
        sql = "insert into " + self.RAND_PROBLEM_INFO_TABLE + " (" + \
            ",".join(self.RAND_PROBLEM_INFO_FIELDS) + ") values('%s', %s, %s, %s, '%s')" \
            % (user, lc_number, status, coins, date)
        return self._add(sql)

    def load_rand_problem_info_by_day(self, date):
        if not self._connect_mysql():
            return False
        sql = "select *  from " + self.RAND_PROBLEM_INFO_TABLE + \
            " where create_time = '%s'" % date
        return self._query(sql)

    def load_rand_problem_infos(self, pn, rn):
        if not self._connect_mysql():
            return False
        sql = "select *  from " + self.RAND_PROBLEM_INFO_TABLE + \
            " order by create_time desc limit %s, %s" % (pn, rn)
        return self._query(sql)

    def update_rand_problem_status(self, id, status):
        if not self._connect_mysql():
            return False
        sql = "update " + self.RAND_PROBLEM_INFO_TABLE + \
            " set status = %s where id = %s" % (status, id)
        return self._update(sql)

    def load_interview_problems(self, pn, rn, pt=-1):
        if pt >= len(problem_types):
            return []
        if not self._connect_mysql():
            return False
        if pt == -1:
            sql = "select * from " + self.INTERVIEW_PROBLEM_INFO_TABLE + \
                " limit %s, %s" % (pn, rn)
        else:
            pt = problem_types[pt]
            sql = "select * from " + self.INTERVIEW_PROBLEM_INFO_TABLE + \
                " where type = '%s' limit %s, %s" % (pt, pn, rn)
        return self._query(sql)

    def add_interview_problem(self, content, answer, problem_type, company, jd):
        if not self._connect_mysql():
            return False
        sql = "insert into " + self.INTERVIEW_PROBLEM_INFO_TABLE + " (" + \
            ",".join(self.INTERVIEW_PROBLEM_INFO_FIELDS) + ") values('%s', '%s', '%s', '%s', '%s')" \
            % (content, answer, problem_type, company, jd)
        return self._add(sql)

    def update_interview_problem_answer(self, id, answer):
        sql = "update " + self.INTERVIEW_PROBLEM_INFO_TABLE + \
            " set answer = %s where id = %s" % (answer, id)
        return self._update(sql)

    def update_interview_problem_jd(self, id, jd):
        sql = "update " + self.INTERVIEW_PROBLEM_INFO_TABLE + \
            " set jd = %s where id = %s" % (jd, id)
        return self._update(sql)

    def _add(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            return True
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            self.cur.close()
            self.conn.close()
            return False

    def _query(self, sql):
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            self.cur.close()
            self.conn.close()
            return data
        except Exception as e:
            logger.error(e)
            self.cur.close()
            self.conn.close()
            return None

    def _update(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            return True
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            self.cur.close()
            self.conn.close()
            return False


if __name__ == '__main__':
    import award
    user = 'smilecode-2'
    lc_number = 1234
    coins = 4
    status = 1
    date = '2022-11-19'
    obj = MysqlService()
    # obj.add_rand_problem_record(user, lc_number, coins, status, date)
    res = obj.load_feedback_info(1, 10)
    print(res)

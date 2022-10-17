#coding=utf-8
import pymysql
from loghandle import logger
import sys

class mysqlService(object):
    """
    table list
    """
    ACCOUNT_INFO_TABLE = 'account_info'
    USER_LC_DAILY_INFO_TABLE = 'user_lc_daily_info'
    USER_LC_DAILY_INFO_FIELDS = ['user', 'total_solve', 'code_submit', 
            'problem_submit', 'rating_score', 'continue_days',
            'new_solve', 'date_time']
    ACCOUNT_INFO_FIELDS = ['user', 'git_account', 'medal']

    def __init__(self):
        self.port = 3306
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'qscool'
        self.db = 'leetcode'
        self.conn = None
        self.cur = None
        self._connect_mysql()
        if not self.conn:
            sys.exit(1)

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
    
    def add_user_daily_info(self, date, datalist):
        presql = "insert into " + self.USER_LC_DAILY_INFO_TABLE
        presql += " (" + ",".join(self.USER_LC_DAILY_INFO_FIELDS) + ")"   
        for data in datalist:
            user = data[0]
            total = int(data[1])
            code_submit = int(data[2])
            problem_submit = int(data[3])
            score = int(data[4])
            days = int(data[5])
            new_solve = int(data[6])
            sql = presql + "values ('%s',%s, %s, %s, %s, %s, %s, '%s')" % \
                (user, total, code_submit, problem_submit, score, \
                    days, new_solve, date)
            logger.info(sql)
            try:
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as e:
                logger.error(e)
                self.conn.rollback()
                self.cur.close()
                self.conn.close()
                return False
        self.cur.close()
        self.conn.close()
        return True

    def load_user_daily_info(self, date):
        sql = "select " + ",".join(self.USER_LC_DAILY_INFO_FIELDS) + \
            " from " + self.USER_LC_DAILY_INFO_TABLE + " where date_time = '%s'" % date
        try:
            self.cur.execute(sql)
            res = {}
            for data in self.cur.fetchall():
                res[data[0]] = data
            return res
        except Exception as e:
            logger.error(e)
            self.cur.close()
            self.conn.close()
            return None

    def update_user_medal(self, user, medal):
        sql = "update " + self.ACCOUNT_INFO_TABLE + " set medal = %s \
            where user = '%s'" % (medal, user)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            self.cur.close()
            self.conn.close()
            return False

    def add_account_info(self, user, git_user, medal=0):
        sql = "insert into " + self.ACCOUNT_INFO_TABLE + " (" + \
            ",".join(self.ACCOUNT_INFO_FIELDS) + ") values('%s', '%s', %s)" \
                % (user, git_user, medal)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            self.cur.close()
            self.conn.close()
            return False

    def load_account_info(self):
        sql = "select " + ",".join(self.ACCOUNT_INFO_FIELDS) + \
            " from " + self.ACCOUNT_INFO_TABLE
        try:
            self.cur.execute(sql)
            user_to_git = {}
            user_medal = {}
            for data in self.cur.fetchall():
                user_to_git[data[0]] = data[1]
                user_medal[data[0]] = data[2]
            return user_to_git, user_medal
        except Exception as e:
            logger.error(e)
            self.cur.close()
            self.conn.close()
            return None, None

if __name__ == '__main__':
    obj = mysqlService()
    date = '2022-10-17'
    res = obj.load_user_daily_info(date)
    print(res)
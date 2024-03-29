"""数据库交互接口"""
import pymysql
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from loghandle import logger


class Dao(object):
    port = 3306
    host = 'localhost'
    user = 'root'
    passwd = 'qscool'
    db = 'leetcode'
    
    def __init__(self):
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
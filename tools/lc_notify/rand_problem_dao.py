"""sql object for each table"""
import settings
import datetime
from dao import Dao
from loghandle import logger

class RandProblemRecord:
    def __init__(self):
        self.id = 0
        self.user = ''
        self.lc_number = 0
        self.coins = 0
        self.status = 1
        self.create_time = ''
        
    def as_dict(self):
        return {
            'id': self.id,
            'user': self.user,
            'lc_number' : self.lc_number,
            'coins': self.coins,
            'create_time': str(self.create_time),
            'status': self.status,
        }


class DaoRandProblem(Dao):
    RAND_PROBLEM_INFO_TABLE = 'rand_problem_info'
    RAND_PROBLEM_INFO_FIELDS = [
        'user', 'lc_number', 'status', 'coins', 'create_time']
    
    def __init__(self):
        pass
    
    def add_rand_problem_record(self, item):
        if not self._connect_mysql():
            return False
        sql = "insert into " + self.RAND_PROBLEM_INFO_TABLE + " (" + \
            ",".join(self.RAND_PROBLEM_INFO_FIELDS) + ") values('%s', %s, %s, %s, '%s')" \
            % (item.user, item.lc_number, item.status, item.coins, item.create_time)
        return self._add(sql)

    def load_rand_problem_info_by_day(self, date):
        if not self._connect_mysql():
            return False
        sql = "select *  from " + self.RAND_PROBLEM_INFO_TABLE + \
            " where create_time = '%s'" % date
        datas = self._query(sql)
        if not datas:
            return None
        resp = []
        for data in datas:
            item = RandProblemRecord()
            item.id = data[0]
            item.user = data[1]
            item.lc_number = data[2]
            item.status = data[3]
            item.coins = data[4]
            item.create_time = data[5]
            resp.append(item)
        return resp

    def load_rand_problem_infos(self, pn, rn):
        if not self._connect_mysql():
            return False
        sql = "select *  from " + self.RAND_PROBLEM_INFO_TABLE + \
            " order by create_time desc limit %s, %s" % (pn, rn)
        datas = self._query(sql)
        if not datas:
            return None
        resp = []
        for data in datas:
            item = RandProblemRecord()
            item.id = data[0]
            item.user = data[1]
            item.lc_number = data[2]
            item.status = data[3]
            item.coins = data[4]
            item.create_time = data[5]
            resp.append(item)
        return resp

    def update_rand_problem_status(self, id, status):
        if not self._connect_mysql():
            return False
        sql = "update " + self.RAND_PROBLEM_INFO_TABLE + \
            " set status = %s where id = %s" % (status, id)
        return self._update(sql)
    
"""sql object for each table"""
import sys
sys.path.append('..')
from dao.dao import Dao


class TargetRecord:
    def __init__(self):
        self.id = 0
        self.user = ''
        self.target_type = 0
        self.target_value = 0
        self.opponent = ''
        self.status = 1
        self.create_date = ''
        self.dead_line = ''
        self.level = 0
        
    def as_dict(self):
        return {
            'user': self.user,
            'target_type' : self.target_type,
            'target_value': self.target_value,
            'opponent': self.opponent,
            'status': self.status,
            'create_date': str(self.create_date),
            'dead_line': str(self.dead_line),
            'level': self.level
        }


class DaoTargetInfo(Dao):
    USER_ATGERT_INFO_TABLE = 'user_target_info'
    USER_ATGERT_INFO_FIELDS = ['user', 'target_type', 'target_value', 'opponent',
                               'status', 'create_date', 'dead_line', 'level']
    
    def __init__(self):
        pass
    
    def add_user_target(self, item):
        if not self._connect_mysql():
            return False
        sql = "insert into " + self.USER_ATGERT_INFO_TABLE + " (" + \
            ",".join(self.USER_ATGERT_INFO_FIELDS) + ") values('%s', %s, %s, '%s', %s, '%s', '%s', '%s')" \
            % (item.user, item.target_type, item.target_value, item.opponent, item.status, item.create_date, item.dead_line, item.level)
        return self._add(sql)

    def load_all_unfinished_target_info(self):
        if not self._connect_mysql():
            return False
        sql = "select * " + \
            " from " + self.USER_ATGERT_INFO_TABLE + " where status = 1"
        datas = self._query(sql)
        if not datas:
            return None
        resp = []
        for data in datas:
            item = TargetRecord()
            item.id = data[0]
            item.user = data[1]
            item.target_type = data[2]
            item.target_value = data[3]
            item.opponent = data[4]
            item.status = data[5]
            item.create_date = data[6]
            item.dead_line = data[7]
            item.level = data[8]
            resp.append(item)
        return resp

    def load_single_user_unfinished_target_info(self, user):
        if not self._connect_mysql():
            return False
        sql = "select * " + \
            " from " + self.USER_ATGERT_INFO_TABLE + \
            " where status = 1 and user = '%s'" % user
        datas =  self._query(sql)
        if not datas:
            return []
        resp = []
        for data in datas:
            item = TargetRecord()
            item.id = data[0]
            item.user = data[1]
            item.target_type = data[2]
            item.target_value = data[3]
            item.opponent = data[4]
            item.status = data[5]
            item.create_date = data[6]
            item.dead_line = data[7]
            item.level = data[8]
            resp.append(item)
        return resp

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
        datas = self._query(sql)
        if not datas:
            return []
        resp = []
        for data in datas:
            item = TargetRecord()
            item.user = data[0]
            item.target_type = data[1]
            item.target_value = data[2]
            item.opponent = data[3]
            item.status = data[4]
            item.create_date = data[5]
            item.dead_line = data[6]
            item.level = data[7]
            resp.append(item)
        return resp
    
    def get_all_targets_befor_day(self, day):
        if not self._connect_mysql():
            return False
        sql = "select * from " + self.USER_ATGERT_INFO_TABLE + \
            " where dead_line <= '%s' and status = 1" % day
        datas = self._query(sql)
        if not datas:
            return []
        resp = []
        for data in datas:
            item = TargetRecord()
            item.id = data[0]
            item.user = data[1]
            item.target_type = data[2]
            item.target_value = data[3]
            item.opponent = data[4]
            item.status = data[5]
            item.create_date = data[6]
            item.dead_line = data[7]
            item.level = data[8]
            resp.append(item)
        return resp
    
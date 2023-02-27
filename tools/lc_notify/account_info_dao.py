"""sql object for each table"""
import settings
import datetime
from dao import Dao
from loghandle import logger

class AccountInfoRecord:
    def __init__(self):
        self.user = ''
        self.git_account = ''
        self.medal = 0
        self.award = 0
        self.email = ''
        self.coins = 0
        self.status = 0
        self.token = 0
        self.date_time = ''
        
    def as_dict(self):
        return {
            'user' : self.user,
            'git_account': self.git_account,
            'medal': self.medal,
            'award': self.award,
            'email': self.email,
            'coins': self.coins,
            'status': self.status,
            'token': self.token,
            'date_time': str(self.date_time)
        }


class DaoAccountInfo(Dao):
    ACCOUNT_INFO_FIELDS = ['user', 'git_account',
              'medal', 'award', 'email', 'date_time', 'coins',
              'status', 'token']
    ACCOUNT_INFO_TABLE = 'account_info'
    
    def __init__(self):
        pass
    
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

    def update_user_token(self, user, token):
        if not self._connect_mysql():
            return False
        sql = "update " + self.ACCOUNT_INFO_TABLE + " set token = '%s' \
            where user = '%s'" % (token, user)
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

    def add_account_info(self, item):
        if not self._connect_mysql():
            return False
        sql = "insert into " + self.ACCOUNT_INFO_TABLE + " (" + \
            ",".join(self.ACCOUNT_INFO_FIELDS) + ") values('%s', '%s', %s, %s, '%s', '%s', %s, %s, '%s')" \
            % (item.user, item.git_account, item.medal, item.award, item.email, item.date_time, item.coins, item.status, item.token)
        return self._add(sql)

    def search_account(self, user):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.ACCOUNT_INFO_FIELDS) + " from " + \
            self.ACCOUNT_INFO_TABLE + " where user = '%s'" % user
        datas = self._query(sql)
        if not datas:
            return None
        for data in datas:
            item = AccountInfoRecord()
            item.user = data[0]
            item.git_account = data[1]
            item.medal = data[2]
            item.award = data[3]
            item.email = data[4]
            item.date_time = data[5]
            item.coins = data[6]
            item.status = data[7]
            item.token = data[8]
            return item
        return None

    def load_all_email_users(self):
        if not self._connect_mysql():
            return False
        sql = "select user, email from " + self.ACCOUNT_INFO_TABLE + \
            " where email != '' and status = 0"
        datas =  self._query(sql)
        if not datas:
            return []
        resp = []
        for data in datas:
            resp.append(data)
        return resp

    def load_all_account_infos(self):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.ACCOUNT_INFO_FIELDS) + \
            " from " + self.ACCOUNT_INFO_TABLE + " where status < 1"
        datas = self._query(sql)
        if not datas:
            return None
        resp = {}
        for data in datas:
            item = AccountInfoRecord()
            item.user = data[0]
            item.git_account = data[1]
            item.medal = data[2]
            item.award = data[3]
            item.email = data[4]
            item.date_time = data[5]
            item.coins = data[6]
            item.status = data[7]
            item.token = data[8]
            resp[item.user] = item
        return resp

    def load_all_accounts(self):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.ACCOUNT_INFO_FIELDS) + \
            " from " + self.ACCOUNT_INFO_TABLE
        datas = self._query(sql)
        if not datas:
            return None
        resp = {}
        for data in datas:
            item = AccountInfoRecord()
            item.user = data[0]
            item.git_account = data[1]
            item.medal = data[2]
            item.award = data[3]
            item.email = data[4]
            item.date_time = data[5]
            item.coins = data[6]
            item.status = data[7]
            item.token = data[8]
            resp[item.user] = item
        return resp

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
    
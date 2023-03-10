import datetime
import sys
sys.path.append('..')
sys.path.append('../dao')
from dao.daily_info_dao import DaoDailyInfo
from dao.account_info_dao import AccountInfoRecord, DaoAccountInfo
from lc_service import LeetcodeService
from loghandle import logger
from lc_error import ErrorCode
from award import MedalType


class AccountService(object):
    def __init__(self):
        self.daoDailyInfo = DaoDailyInfo()
        self.daoAccount = DaoAccountInfo()
        self.leetcode_service = LeetcodeService()
        self._default_coins = 100
        self._knight_award_coins = 30
        self._guarding_award_coins = 50

    def submit_account_info(self, lc_account, git_account='', email=''):
        ret = ['0', "succ"]
        blanks = [' ', '\t', '\n']
        for c in lc_account:
            if c in blanks:
                ret[0] = ErrorCode.ACCOUNT_NOT_EXIST
                ret[1] = ErrorCode.error_message(ret[0])
                return ret
        if email and '@' not in email:
            ret[0] = ErrorCode.EMAIL_FORMAT_ERROR
            ret[1] = ErrorCode.error_message(ret[0])
            return ret
        userDailyInfo = self.leetcode_service.get_user_lc_stat_info(lc_account)
        if not userDailyInfo:
            ret[0] = ErrorCode.ACCOUNT_NOT_EXIST
            ret[1] = ErrorCode.error_message(ret[0])
            return ret
        userinfo = self.daoAccount.search_account(lc_account)
        if not userinfo:  # 添加新用户信息，并添加最新的统计信息
            logger.info("add lc_account: " + lc_account)
            item = AccountInfoRecord()
            item.coins = self._default_coins
            medal = self.leetcode_service.get_user_medal_info(lc_account)
            if medal == MedalType.Knight:
                item.coins += self._knight_award_coins
            elif medal == MedalType.Guardian:
                medal = 3
                item.coins += self._knight_award_coins + self._guarding_award_coins
            item.user = lc_account
            item.git_account = git_account if git_account else ''
            item.email = email if email else ''
            item.medal = medal if medal else 0
            item.date_time = datetime.date.today()
            if not self.daoAccount.add_account_info(item):
                ret[0] = ErrorCode.MYSQL_SERVICE_ERR
                ret[1] = ErrorCode.error_message(ret[0])
                return ret
            
            score = self.leetcode_service.get_user_score_info(lc_account)
            userDailyInfo.rating_score = score
            userDailyInfo.continue_days = 1
            userDailyInfo.new_solve = 0
            userDailyInfo.total_days = 1
            userDailyInfo.date_time = datetime.date.today()
            if not self.daoDailyInfo.add_single_user_daily_info(userDailyInfo):
                ret[0] = ErrorCode.MYSQL_SERVICE_ERR
                ret[1] = ErrorCode.error_message(ret[0])
                return ret
        else:
            u_email = userinfo.email
            u_git = userinfo.git_account
            res = True
            if lc_account != '' and email == '' and git_account == '':
                ret[0] = ErrorCode.ACCOUNT_EXIST
                ret[1] = ErrorCode.error_message(ret[0])
                return ret
            if u_email == '' and email != '':
                logger.info(lc_account + " update email: " + email)
                res = self.daoAccount.update_user_email(lc_account, email)
            if u_git == '' and git_account != '':
                logger.info(lc_account + " update git_account: " + git_account)
                res = self.daoAccount.update_user_git_account(lc_account, git_account)
            if not res:
                ret[0] = ErrorCode.MYSQL_SERVICE_ERR
                ret[1] = ErrorCode.error_message(ret[0])
                return ret
        return ret
    

if __name__ == '__main__':
    lc_account = 'smilecode-2'
    email = ''
    git_account = '123'
    obj = AccountService()
    res = obj.submit_account_info(lc_account)
    print(res)
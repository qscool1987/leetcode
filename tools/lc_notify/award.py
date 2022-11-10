"""
激励触发模块
当用户满足某个激励条件时将触发邮件通知机制
"""
import email_service
import settings
from loghandle import logger
import mysql_service
import lc_service
import random


class MedalType:
    """
    奖励类型
    """
    Knight = 1
    Guardian = 2
    CodeSubmit = 4
    ProblemSubmit = 8
    ContinueDays = 16


class LcAward(object):
    CodeSubmitNum = 1000
    ProblemSubmitNum = 50
    ContinueDaysNum = 100
    Congratulations = {
        MedalType.Knight: "恭喜你，上Knight了!!!",
        MedalType.Guardian: "恭喜你，上Guardian了!!!",
        MedalType.CodeSubmit: "恭喜你，push代码提交超过1000行了!!!",
        MedalType.ProblemSubmit: "恭喜你，push题量超过50题了!!!",
        MedalType.ContinueDays: "恭喜你，连续打卡超过100天了!!!"
    }
    award_str = """
        \n为了表示鼓励，有一份小礼物要送给你，辛苦填写一下快递地址，收件人信息和电话号码～ \
        回复此邮件即可!!\n 请放心，所有信息会严格保密。"""

    def __init__(self,
                 medal_history,
                 user_award,
                 user_email,
                 sql_service,
                 leetcode_service):
        self.medal_history = medal_history  # 用户的历史medal记录 例如 3=1+2说明该用户已经上k，上g
        self.user_award = user_award  # 用户是否已经发放过奖励 1表示发放过，0表示没有
        self.user_email = user_email
        self.leetcode_service = leetcode_service
        self.sql_service = sql_service  # 数据库服务对象
        self.emailobj = email_service.EmailService()

    def deal_award(self, td_info):
        """"
        处理奖励
        bit位表示奖励触发条件是否满足，如果同一天同事多个条件满足，则选择最低bit位发放
        """
        user = td_info[0]
        if user not in self.user_email:  # 没有提供邮件的就只能遗憾了
            return
        td_medal = 0
        medal = self.leetcode_service.get_user_medal_info(user)  # 获取用户当前lc奖牌信息
        if medal == 1:
            td_medal = 1
        elif medal == 2:
            td_medal = 3  # 如果上g，则自动认为已经完成上k的条件
        if td_info[2] >= self.CodeSubmitNum:
            td_medal += settings.MedalType.CodeSubmit
        if td_info[3] >= self.ProblemSubmitNum:
            td_medal += settings.MedalType.ProblemSubmit
        if td_info[5] >= self.ContinueDaysNum:
            td_medal += settings.MedalType.ContinueDays
        if td_medal <= self.medal_history[user]:
            return
        td_award = self.medal_history[user] ^ td_medal
        td_award = td_award & (-td_award)  # 取最低bit位的奖励进行发放
        to_addr = self.user_email[user]
        if self.user_award[user] == 0:
            if self._rand_hit_award():  # 概率中奖
                bodystr = self.Congratulations[td_award] + self.award_str
                self.emailobj.send_email(to_addr, bodystr)
                self.sql_service.update_user_award(user, 1)
                logger.info(
                    "send email to {} for award congratuation".format(user))
            else:
                bodystr = self.Congratulations[td_award]
                self.emailobj.send_email(to_addr, bodystr)
                logger.info(
                    "send email to {} for stage congratuation".format(user))
        elif self.user_award[user] == 1:
            bodystr = self.Congratulations[td_award]
            self.emailobj.send_email(to_addr, bodystr)
            logger.info(
                "send email to {} for stage congratuation".format(user))
        sql_service.update_user_medal(user, td_medal)

    def _rand_hit_award(self):
        k1 = random.randint(1, 100)
        k2 = random.randint(1, 100)
        mul = k1 * k2
        if mul >= 10 and mul % 10 == 0:
            return True
        return False


if __name__ == '__main__':
    user = 'smilecode-2'
    medal_history = {}
    medal_history[user] = 4
    user_award = {}
    user_award[user] = 1
    user_email = {}
    user_email[user] = "595949643@qq.com"
    sql_service = mysql_service.MysqlService()
    leetcode_service = lc_service.LeetcodeService()
    obj = LcAward(medal_history,
                  user_award,
                  user_email,
                  sql_service,
                  leetcode_service)
    info = ['smilecode-2', 724, 14406, 15, 1815, 100, 4, 1]
    # obj.deal_award(info)

    print(obj._rand_hit_award())

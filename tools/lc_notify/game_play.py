"""
管理游戏币的各种奖励，惩罚事件
"""
import mysql_service
import award
import lc_target
import json
import random
import datetime
import email_service
import lc_service
import settings

from loghandle import logger


class CoinEvent:
    events = {
        1: "Knight",
        2: "Guardian",
        3: "ProblemSubmit",
        4: "DailyProblemFinish",
        5: "DailyTop",
        6: "TargetSucc",
        7: "RandomProblemFinish",
        8: "DailyProblemUnfinsh",
        9: "TargetFail",
        10: "RandomProblemUnfinish"
    }


class GamePlay(object):
    PNUM_START = 1
    PUNM_END = 2800

    def __init__(self, award_service=None, tday_infos={}, yday_infos={}):
        self.sql_service = mysql_service.MysqlService()
        self.award_service = award_service  # 奖励服务
        self.target_service = lc_target.TargetService(
            self.sql_service, self)  # 目标服务
        self.tday_infos = tday_infos
        self.yday_infos = yday_infos
        self.td_user_infos = {}
        self.yd_user_infos = {}
        self.user_td_coins = {}

    def run(self, day):
        self.deal_daily_coins()
        self._deal_award()
        logger.info("deal award finished")
        self.target_service.deal_all_targets_status()
        logger.info("deal target finished")
        self.check_rand_problem_finish(day)
        logger.info("deal rand problem finished")
        self._update_user_coins()
        logger.info("update coins finished")
        logger.info(json.dumps(self.user_td_coins))
        self._update_user_account_status()
        logger.info("update account status finished")

    def _update_user_coins(self):
        for u in self.user_td_coins:
            coins = self.sql_service.search_user_coins(u)
            if not coins:
                continue
            coins += self.user_td_coins[u]
            self.sql_service.update_user_coins(u, coins)

    def deal_daily_coins(self):
        # 23点后根据用户今日信息进行判断
        for user in self.tday_infos:
            info = self.tday_infos[user]
            item = {}
            for i in range(0, len(self.sql_service.USER_LC_DAILY_INFO_FIELDS)-1):
                key = self.sql_service.USER_LC_DAILY_INFO_FIELDS[i]
                item[key] = info[i]
            self.td_user_infos[user] = item
        for user in self.yday_infos:
            info = self.yday_infos[user]
            item = {}
            for i in range(0, len(self.sql_service.USER_LC_DAILY_INFO_FIELDS)-1):
                key = self.sql_service.USER_LC_DAILY_INFO_FIELDS[i]
                item[key] = info[i]
            self.yd_user_infos[user] = item

        for user in self.td_user_infos:
            self.user_td_coins[user] = self._calculate_user_add_coins(user)
        items = self.td_user_infos.items()
        items = sorted(
            items, key=lambda data: data[1]['new_solve'], reverse=True)
        solve_num_list = []
        for i in range(0, len(items)):
            score = items[i][1]['new_solve']
            if score == items[i][1]['total_solve']:
                continue
            if score >= 100:
                continue
            if score not in solve_num_list:
                solve_num_list.append(score)
            if len(solve_num_list) >= 3:
                break
        for i in range(0, len(solve_num_list)):
            score = solve_num_list[i]
            for item in items:
                if item[1]['new_solve'] == score:
                    self.add_user_coins(item[0], 3-i)

    def _update_user_account_status(self):
        for user in self.td_user_infos:
            td_info = self.td_user_infos[user]
            if td_info['lazy_days'] >= settings.LazyLevel.LEVEL16:
                self.sql_service.update_account_status(user, 1)

    def _calculate_user_add_coins(self, user):
        td_info = None
        yd_info = None
        if user in self.td_user_infos:
            td_info = self.td_user_infos[user]
        if user in self.yd_user_infos:
            yd_info = self.yd_user_infos[user]
        if not td_info:
            return None
        add_n = 0
        delt_problem_submit = td_info['problem_submit']
        delt_new_solve = td_info['total_solve']
        if not yd_info:
            delt_new_solve = td_info['new_solve']
        else:
            delt_new_solve = td_info['total_solve'] - yd_info['total_solve']
            delt_problem_submit -= yd_info['problem_submit']
        if delt_new_solve > 0 and delt_new_solve < 100:
            add_n += 1
        elif delt_new_solve == 0:
            add_n -= 1
        add_n += delt_problem_submit * 3
        return add_n

    def _deal_award(self):
        for u in self.tday_infos:
            td_award = self.award_service.deal_award(self.tday_infos[u])
            if not td_award:
                continue
            if td_award == award.MedalType.Knight:
                self.user_td_coins[u] += 30
            elif td_award == award.MedalType.Guardian:
                self.user_td_coins[u] += 50

    def add_user_coins(self, user, coins):
        self.user_td_coins[user] += coins

    def publish_rand_problem(self, td):  # 每天6点发布
        """抽题指定随机用户完成"""
        pid = random.randint(self.PNUM_START, self.PUNM_END)
        coins = random.randint(3, 5)
        users = self.sql_service.load_all_email_users()
        k1 = random.randint(1, len(users))
        k2 = random.randint(1, len(users))
        user1 = users[k1-1][0]
        email1 = users[k1-1][1]
        self.sql_service.add_rand_problem_record(user1, pid, coins, 1, td)
        bodystr = "恭喜！！\n你被随机抽中参与今天的幸运答题，leetcode题号为：" + \
            str(pid) + "，完成后可获得：" + str(coins) + \
            "积分奖励！！\n请于今天24点之前完成，否则要扣除1个积分哦！！"
        email_service.EmailService.send_email(email1, bodystr)
        if k2 == k1:
            return
        user2 = users[k2-1][0]
        email2 = users[k2-1][1]
        self.sql_service.add_rand_problem_record(user2, pid, coins, 1, td)
        email_service.EmailService.send_email(email2, bodystr)

    def check_rand_problem_finish(self, td):
        infos = self.sql_service.load_rand_problem_info_by_day(td)
        leetcode_service = lc_service.LeetcodeService()
        for data in infos:
            id = data[0]
            user = data[1]
            lc_number = data[2]
            coins = data[4]
            status = leetcode_service.check_user_rand_problem_status(
                user, lc_number, td)
            if status == 2:
                self.add_user_coins(user, coins)
            else:
                self.add_user_coins(user, -1)
            self.sql_service.update_rand_problem_status(id, status)


if __name__ == '__main__':
    leetcode_service = lc_service.LeetcodeService()
    obj = GamePlay()
    td = '2022-11-21'
    infos = obj.sql_service.load_rand_problem_info_by_day(td)
    print(infos)
    for data in infos:
        id = data[0]
        user = data[1]
        lc_number = data[2]
        coins = data[4]
        status = leetcode_service.check_user_rand_problem_status(
            user, lc_number, td)
        print(user, status)

"""
管理游戏币的各种奖励，惩罚事件
"""
import award
import award
import lc_target
import json
import random
import datetime
import email_service
import lc_service
import settings
from target_info_dao import TargetRecord, DaoTargetInfo
from rand_problem_dao import RandProblemRecord, DaoRandProblem
from interview_problem_dao import InterviewProblemRecord, DaoInterviewProblem
from feedback_dao import FeedbackRecord, DaoFeedback
from daily_info_dao import DaoDailyInfo, UserDailyInfoRecord
from account_info_dao import AccountInfoRecord, DaoAccountInfo

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
    PUNM_END = 2489
    TOPN = 5
    UPSCORE = 10

    def __init__(self, tday_infos={}, yday_infos={}):
        self.award_service = award.LcAward()  # 奖励服务
        self.target_service = lc_target.TargetService(self)  # 目标服务
        self.td_user_infos = tday_infos
        self.yd_user_infos = yday_infos
        self.user_td_coins = {}
        self.dao_account = DaoAccountInfo()
        self.dao_daily_info = DaoDailyInfo()
        self.dao_rand_problem = DaoRandProblem()

    def run(self, day):
        self.deal_daily_coins()
        self._deal_award()
        logger.info("deal award finished")
        self.target_service.deal_all_targets_status()
        logger.info("deal target finished")
        self.check_rand_problem_finish(day)
        logger.info("deal rand problem finished")
        print(json.dumps(self.user_td_coins))
        self._update_user_coins()
        logger.info("update coins finished")
        logger.info(json.dumps(self.user_td_coins))
        self._update_user_account_status()
        logger.info("update account status finished")

    def _update_user_coins(self):
        for u in self.user_td_coins:
            coins = self.dao_account.search_user_coins(u)
            if not coins:
                continue
            coins += self.user_td_coins[u]
            self.dao_account.update_user_coins(u, coins)

    def deal_daily_coins(self):
        # 23点后根据用户今日信息进行判断
        for user in self.td_user_infos:
            self.user_td_coins[user] = self._calculate_user_add_coins(user)

        items = self.td_user_infos.values()
        items = sorted(
            items, key=lambda data: data.new_solve, reverse=True)
        solve_num_list = []
        except_users = set()
        for item in items:
            user = item.user
            score = item.new_solve  # 用户今日刷题量
            if score >= item.total_solve:  # 今日新加入的，或者近日重新复活的
                except_users.add(user)
                continue
            if score >= 60 or score <= 0:  # 除去异常数据
                continue
            if score not in solve_num_list:
                solve_num_list.append(score)
            if len(solve_num_list) >= self.TOPN:
                break
        for i in range(0, len(solve_num_list)):
            score = solve_num_list[i]
            for item in items:
                user = item.user
                if user in except_users:
                    continue
                if item.new_solve < score:
                    break
                if item.new_solve == score:
                    self.add_user_coins(user, self.UPSCORE - i*2)

    def _update_user_account_status(self):
        for user in self.td_user_infos:
            td_info = self.td_user_infos[user]
            if td_info.rating_score >= 2300 or td_info.total_solve >= 2500:
                continue
            if td_info.lazy_days >= settings.LazyLevel.LEVEL16:
                self.dao_account.update_account_status(user, 1)

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
        add_score = 0
        delt_new_solve = td_info.total_solve
        if not yd_info:  # 当天新加入的玩家送1分,因为没有历史数据
            delt_new_solve = td_info.new_solve
            add_score = 1
        else:  # 否则按题目难度统计得分
            delt_new_solve = td_info.total_solve - yd_info.total_solve
            if delt_new_solve > 0 and delt_new_solve < 100:  # 异常情况 排出
                # add_n += 1
                add_score += td_info.hard_num * 3
                add_score += td_info.mid_num * 2
                add_score += td_info.easy_num
            elif delt_new_solve == 0:
                # add_n -= 1
                add_score = 0
        return add_score

    def _deal_award(self):
        for u in self.td_user_infos:
            td_award = self.award_service.deal_award(self.td_user_infos[u])
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
        users = self.dao_account.load_all_email_users()
        k1 = random.randint(1, len(users))
        k2 = random.randint(1, len(users))
        user1 = users[k1-1][0]
        email1 = users[k1-1][1]
        item = RandProblemRecord()
        item.user = user1
        item.lc_number = pid
        item.coins = coins
        item.status = 1
        item.create_time = td
        self.dao_rand_problem.add_rand_problem_record(item)
        bodystr = "恭喜！！\n你被随机抽中参与今天的幸运答题，leetcode题号为：" + \
            str(pid) + "，完成后可获得：" + str(coins) + \
            "积分奖励！！\n请于今天24点之前完成，否则要扣除1个积分哦！！"
        email_service.EmailService.send_email(email1, bodystr)
        if k2 == k1:
            return
        user2 = users[k2-1][0]
        email2 = users[k2-1][1]
        item2 = RandProblemRecord()
        item2.user = user2
        item2.lc_number = pid
        item2.coins = coins
        item2.status = 1
        item2.create_time = td
        self.dao_rand_problem.add_rand_problem_record(item2)
        email_service.EmailService.send_email(email2, bodystr)

    def check_rand_problem_finish(self, td):
        infos = self.dao_rand_problem.load_rand_problem_info_by_day(td)
        leetcode_service = lc_service.LeetcodeService()
        for data in infos:
            id = data.id
            user = data.user
            lc_number = data.lc_number
            coins = data.coins
            status = leetcode_service.check_user_rand_problem_status(
                user, lc_number, td)
            if status == 2:
                self.add_user_coins(user, coins)
            else:
                self.add_user_coins(user, -1)
            self.dao_rand_problem.update_rand_problem_status(id, status)


if __name__ == '__main__':
    leetcode_service = lc_service.LeetcodeService()
    obj = GamePlay()
    td = '2022-11-21'
    obj.publish_rand_problem(td)

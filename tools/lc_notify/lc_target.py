"""
目标服务类
1.评估用户目标等级
2.处理目标完成状态

"""
from math import ceil, floor
from loghandle import logger
import datetime
from dateutil.parser import parse
from lc_error import ErrorCode
import email_service
from loghandle import logger
from daily_info_dao import DaoDailyInfo
from target_info_dao import DaoTargetInfo
from account_info_dao import DaoAccountInfo


class TargetType:
    Rank = 1  # 周赛排名
    ProblemSolve = 2  # 总刷题量
    CodeSubmit = 3  # push代码行数
    ProblemSubmit = 4  # push题目数量
    ContinueDays = 5  # 连续打卡天数
    Rating = 6  # 竞赛分数
    Challenge = 7  # 挑战pk

    @classmethod
    def from_type_to_str(cls, target_type):
        if target_type == TargetType.Rank:
            return "周赛排名"
        elif target_type == TargetType.ProblemSolve:
            return "总刷题量"
        elif target_type == TargetType.CodeSubmit:
            return "push代码行数"
        elif target_type == TargetType.ProblemSubmit:
            return "push代码题量"
        elif target_type == TargetType.ContinueDays:
            return "连续打卡天数"
        elif target_type == TargetType.Rating:
            return "竞赛分数"
        elif target_type == TargetType.Challenge:
            return "挑战PK"
        else:
            return "未知类型"

    @classmethod
    def from_str_to_type(cls, target):
        if target == "周赛排名":
            return TargetType.Rank
        elif target == "总刷题量":
            return TargetType.ProblemSolve
        elif target == "push代码行数":
            return TargetType.CodeSubmit
        elif target == "push代码题量":
            return TargetType.ProblemSubmit
        elif target == "连续打卡天数":
            return TargetType.ContinueDays
        elif target == "竞赛分数":
            return TargetType.Rating
        elif target == "挑战PK":
            return TargetType.Challenge
        return 0


class TargetStatus:
    UNKNOW = 0
    PROCESSING = 1
    SUCC = 2
    FAIL = 3

    @classmethod
    def from_str_to_status(cls, status):
        if status == "未知状态":
            return TargetStatus.UNKNOW
        elif status == "进行中":
            return TargetStatus.PROCESSING
        elif status == "已完成":
            return TargetStatus.SUCC
        elif status == "已失败":
            return TargetStatus.FAIL
        return TargetStatus.UNKNOW

    @classmethod
    def from_status_to_str(cls, status):
        if status == TargetStatus.UNKNOW:
            return "未知状态"
        elif status == TargetStatus.PROCESSING:
            return "进行中"
        elif status == TargetStatus.SUCC:
            return "已完成"
        elif status == TargetStatus.FAIL:
            return "已失败"
        return "未知状态"


class TargetLevel:
    UNKNOW = 0
    VERY_EASY = 1  # 5
    EASY = 2     # 10
    MID = 3      # 15
    LITTLE_HARD = 4  # 20
    HARD = 5       # 30
    VERY_HARD = 6   # 45
    UNBELIEVABLE = 7  # 70

    level_to_str = {
        0: "UNKNOW",
        1: "VERY_EASY",
        2: "EASY",
        3: "MID",
        4: "LITTLE_HARD",
        5: "HARD",
        6: "VERY_HARD",
        7: "UNBELIEVABLE"
    }

    level_to_score = {
        0: 0,
        1: 5,
        2: 10,
        3: 15,
        4: 20,
        5: 30,
        6: 45,
        7: 70
    }

    @classmethod
    def from_level_to_score(cls, level):
        if level in TargetLevel.level_to_score:
            return TargetLevel.level_to_score[level]
        return 0

    @classmethod
    def from_level_to_str(cls, level):
        if level in TargetLevel.level_to_str:
            return TargetLevel.level_to_str[level]
        else:
            return "UNKNOW"


class TargetService(object):
    def __init__(self, game_play):
        self.daoDailyInfo = DaoDailyInfo()
        self.daoTarget = DaoTargetInfo()
        self.daoAccount = DaoAccountInfo()
        self.game_play = game_play

    def _deal_challenge_target(self, you, opponent, dead_line):
        you_info = self.daoAccount.search_account(you)
        opponent_info = self.daoAccount.search_account(opponent)
        you_email = you_info.email
        opponent_email = opponent_info.email
        today = str(datetime.date.today())
        you_bodystr = "您已于" + today + "号发起了对 " + opponent + " 的挑战任务，\
            结束时间为" + dead_line + "号。系统将于" + dead_line + "号23点55分计算任务状态，\
            计算规则为比较竞赛分数大小，竞赛分数高者为胜利方，会得到相应积分奖励，失败方则会扣除奖\
            励分数的一半。\n挑战无小事，请您认真准备!!"
        opponent_bodystr = "请注意，" + you + "已于" + today + "号发起了对您的挑战任务，\
            结束时间为" + dead_line + "号。系统将于" + dead_line + "号23点55分计算任务状态，\
            计算规则为比较竞赛分数大小，竞赛分数高者为胜利方，会得到相应积分奖励，失败方则会扣除奖\
            励分数的一半。\n挑战无小事，请您认真应对!!"
        if you_email != '':
            email_service.EmailService.send_email(you_email, you_bodystr)
        if opponent_email != '':
            email_service.EmailService.send_email(
                opponent_email, opponent_bodystr)

    def _delt_days(self, dead_line):
        today = datetime.date.today()
        limit = parse(dead_line)
        today = parse(str(today))
        delt = limit - today
        return delt.days

    def evaluate_target_level(self, user, target_type, target_val=0, opponent='', dead_line=''):
        # 评估目标的困难程度
        nowinfo = self.daoDailyInfo.search_user_recent_info(user)
        if not nowinfo:
            return ErrorCode.ACCOUNT_NOT_EXIST, 0
        level = 0
        errcode = ErrorCode.SUCC
        if target_type == TargetType.Rank:
            pass
        elif target_type == TargetType.ProblemSolve:
            errcode, level = self.evaluate_problem_solve_target_level(
                nowinfo, target_val, dead_line)
        elif target_type == TargetType.CodeSubmit:
            errcode, level = self.evaluate_code_submit_target_level(
                nowinfo, target_val, dead_line)
        elif target_type == TargetType.ProblemSubmit:
            errcode, level = self.evaluate_problem_submit_target_level(
                nowinfo, target_val, dead_line)
        elif target_type == TargetType.ContinueDays:
            errcode, level = self.evaluate_continue_days_target_level(
                nowinfo, target_val, dead_line)
        elif target_type == TargetType.Rating:
            errcode, level = self.evaluate_rating_target_level(
                nowinfo, target_val, dead_line)
        elif target_type == TargetType.Challenge:
            errcode, level = self.evaluate_challenge_target_level(
                nowinfo, opponent, dead_line)
        return errcode, level

    def _cal_delt_days_level(self, delt_days):
        level = 1
        if delt_days >= 15 and delt_days < 30:
            level = 2
        elif delt_days >= 30 and delt_days < 45:
            level = 1.5
        elif delt_days >= 45 and delt_days < 60:
            level = 1.2
        else:
            level = 1
        return level

    def evaluate_problem_solve_target_level(self, nowinfo, target_val, dead_line):
        if nowinfo.total_solve >= target_val:  # 目标不合理
            return ErrorCode.PROBLEM_NUM_OVER, 0
        diff_val = target_val - nowinfo.total_solve
        delt_days = self._delt_days(dead_line)
        avg = diff_val / delt_days
        delt_days_level = self._cal_delt_days_level(delt_days)
        avg = floor(avg / delt_days_level)
        level = 0
        if avg == 0:
            return ErrorCode.AVG_PROBLEM_NUM_SMALL, level
        elif avg == 1:
            level = TargetLevel.VERY_EASY
        elif avg == 2:
            level = TargetLevel.EASY
        elif avg in [3, 4]:
            level = TargetLevel.MID
        elif avg in [5, 6]:
            level = TargetLevel.LITTLE_HARD
        elif avg == 7:
            level = TargetLevel.HARD
        elif avg == 8:
            level = TargetLevel.VERY_HARD
        else:
            level = TargetLevel.UNBELIEVABLE
        return ErrorCode.SUCC, level

    def evaluate_code_submit_target_level(self, nowinfo, target_val, dead_line):
        if nowinfo.code_submit >= target_val:
            return ErrorCode.CODELINE_OVER, 0
        diff_val = target_val - nowinfo.code_submit
        delt_days = self._delt_days(dead_line)
        avg = diff_val / delt_days
        delt_days_level = self._cal_delt_days_level(delt_days)
        avg = floor(avg / delt_days_level)
        level = 0
        if avg < 5:
            return ErrorCode.AVG_CODELINE_NUM_SMALL, 0
        elif avg <= 20:
            level = TargetLevel.VERY_EASY
        elif avg > 20 and avg <= 40:
            level = TargetLevel.EASY
        elif avg > 40 and avg <= 60:
            level = TargetLevel.MID
        elif avg > 60 and avg <= 80:
            level = TargetLevel.LITTLE_HARD
        elif avg > 80 and avg <= 100:
            level = TargetLevel.HARD
        elif avg > 100 and avg <= 120:
            level = TargetLevel.VERY_HARD
        else:
            level = TargetLevel.UNBELIEVABLE
        return ErrorCode.SUCC, level

    def evaluate_problem_submit_target_level(self, nowinfo, target_val, dead_line):
        if nowinfo.problem_submit >= target_val:  # 目标不合理
            return ErrorCode.PROBLEM_SUBMIT_OVER, 0
        diff_val = target_val - nowinfo.problem_submit
        delt_days = self._delt_days(dead_line)
        avg = 3 * diff_val / delt_days
        delt_days_level = self._cal_delt_days_level(delt_days)
        avg = floor(avg / delt_days_level)
        level = 0
        if avg <= 1:
            level = TargetLevel.VERY_EASY
        elif avg == 2:
            level = TargetLevel.MID
        elif avg == 3:
            level = TargetLevel.HARD
        else:
            level = TargetLevel.UNBELIEVABLE
        return ErrorCode.SUCC, level

    def evaluate_continue_days_target_level(self, nowinfo, target_val, dead_line):
        delt_days = self._delt_days(dead_line)
        level = 0
        if delt_days <= 20:
            level = TargetLevel.VERY_EASY
        elif delt_days > 20 and delt_days <= 40:
            level = TargetLevel.EASY
        elif delt_days > 40 and delt_days <= 60:
            level = TargetLevel.MID
        elif delt_days > 60 and delt_days <= 80:
            level = TargetLevel.LITTLE_HARD
        elif delt_days > 80 and delt_days <= 100:
            level = TargetLevel.HARD
        elif delt_days > 100 and delt_days <= 120:
            level = TargetLevel.VERY_HARD
        else:
            level = TargetLevel.UNBELIEVABLE
        return ErrorCode.SUCC, level

    def _cal_rating_level(self, nowscore):
        level = 1
        if nowscore <= 1700:
            level = 1
        elif nowscore > 1700 and nowscore <= 2050:
            level = 2
        elif nowscore > 2050 and nowscore <= 2450:
            level = 3
        else:
            level = 4
        return level

    def _cal_rating_param(self, nowscore, target_val):
        lnow = self._cal_rating_level(nowscore)
        ltarget = self._cal_rating_level(target_val)
        pvar = 1
        if lnow == 1:
            pvar = 1
        elif lnow == 2:
            pvar = 1.25
        elif lnow == 3:
            pvar = 1.5
        else:
            pvar = 2
        delt = ltarget - lnow
        if delt == 0:
            return pvar
        elif delt == 1:
            return pvar * 1.25
        elif delt == 2:
            return pvar * 1.5
        else:
            return pvar * 2

    def _cal_rating_target_level(self, gap_score, gap_days, pvar):
        avg = 7 * gap_score / gap_days  # 每周
        avg = ceil(avg)
        level = 0
        if avg <= 10:
            level = 2
        elif avg > 10 and avg <= 20:
            level = 2.75
        else:
            level = 3.5
        level = ceil(level * pvar)
        if level > TargetLevel.UNBELIEVABLE:
            level = TargetLevel.UNBELIEVABLE
        return level

    def evaluate_rating_target_level(self, nowinfo, target_val, dead_line):
        """
        [1500-1700], (1700,2100], (2100,2500],(2500,-)
        根据当前分数，目标分数，间隔分数，间隔周数来评估目标等级
        当前所处的level  lnow   1-4
        目标所处的level  ltarget 1-4
        间隔分数    gap_score 
        间隔周数    gap_week
        """
        if nowinfo.rating_score >= target_val:  # 目标不合理
            return ErrorCode.RATING_OVER, 0
        if nowinfo.rating_score == 0:
            return ErrorCode.NO_RATING_SCORE, 0
        diff_val = target_val - nowinfo.rating_score
        if diff_val < 50:
            return ErrorCode.RATING_GAP_SMALL, 0
        delt_days = self._delt_days(dead_line)
        if delt_days < 30:
            return ErrorCode.DATETIME_GAP_SHORT2, 0
        nowscore = nowinfo.rating_score
        pvar = self._cal_rating_param(nowscore, target_val)
        level = self._cal_rating_target_level(diff_val, delt_days, pvar)
        return ErrorCode.SUCC, level

    def evaluate_challenge_target_level(self, you, oponent, dead_line):
        other = self.daoDailyInfo.search_user_recent_info(oponent)
        if not other:
            return ErrorCode.OPPNENT_NOT_EXIST, 0
        if you.rating_score == 0:
            return ErrorCode.NO_RATING_SCORE, 0
        if you.rating_score >= other.rating_score:
            return ErrorCode.PK_RATING_OVER, 0
        diff_val = other.rating_score - you.rating_score
        delt_days = self._delt_days(dead_line)
        if delt_days < 30:
            return ErrorCode.DATETIME_GAP_SHORT2, 0
        pvar = 1
        nowscore = you.rating_score
        target_val = other.rating_score
        lv = self._cal_rating_level(target_val)
        if lv == 1:
            target_val = target_val + 0.8 * diff_val
        elif lv == 2:
            target_val = target_val + 0.6 * diff_val
        elif lv == 3:
            target_val = target_val + 0.4 * diff_val
        else:
            target_val = target_val + 0.2 * diff_val
        pvar = self._cal_rating_param(nowscore, target_val)
        level = self._cal_rating_target_level(diff_val, delt_days, pvar)
        self._deal_challenge_target(you.user, other.user, dead_line)
        return ErrorCode.SUCC, level

    def deal_all_targets_status(self):
        target_infos = self.daoTarget.load_all_unfinished_target_info()
        user_infos = {}
        user_accounts = {}
        for target in target_infos:
            id = target.id
            user = target.user
            target_type = target.target_type
            target_value = target.target_value
            opponent = target.opponent
            status = target.status
            dead_line = target.dead_line
            level = target.level
            if target_type == TargetType.Rank:
                pass
            elif target_type == TargetType.ProblemSolve:
                status = self.judge_problem_solve_target(
                    user, target_value, dead_line)
            elif target_type == TargetType.CodeSubmit:
                status = self.judge_code_submit_target(
                    user, target_value, dead_line)
            elif target_type == TargetType.ProblemSubmit:
                status = self.judge_problem_submit_target(
                    user, target_value, dead_line)
            elif target_type == TargetType.ContinueDays:
                status = self.judge_continue_days_target(
                    user, target_value, dead_line)
            elif target_type == TargetType.Rating:
                status = self.judge_rating_target(
                    user, target_value, dead_line)
            elif target_type == TargetType.Challenge:
                status = self.judge_challenge_target(user, opponent, dead_line)
            if status == TargetStatus.SUCC:
                logger.info(
                    "{} finished target_type {} successful!".format(user, target))
            elif status == TargetStatus.FAIL:
                logger.info("{} target_type {} failed!".format(user, target))
            self.daoTarget.update_user_target_status(id, status)
            if status == TargetStatus.SUCC:
                self.game_play.add_user_coins(
                    user, TargetLevel.from_level_to_score(level))
                if target_type == TargetType.Challenge:
                    self.game_play.add_user_coins(
                        opponent, -TargetLevel.from_level_to_score(level) / 2)
            elif status == TargetStatus.FAIL:
                self.game_play.add_user_coins(
                    user, -TargetLevel.from_level_to_score(level) / 2)
                if target_type == TargetType.Challenge:
                    self.game_play.add_user_coins(
                        opponent, TargetLevel.from_level_to_score(level))
            elif status == TargetStatus.PROCESSING and target_type == TargetType.ProblemSolve:
                # 通知用户 抓紧完成目标
                user_account = None
                if user in user_accounts:
                    user_account = user_accounts[user]
                else:
                    user_account = self.daoAccount.search_account(user)
                    user_accounts[user] = user_account
                email_addr = user_account.email
                if email_addr != '':
                    user_info = None
                    if user in user_infos:
                        user_info = user_infos[user]
                    else:
                        user_info = self.daoDailyInfo.search_user_recent_info(
                            user)
                        user_infos[user] = user_info
                    current_problem_solve = user_info.total_solve
                    current_rating_score = user_info.rating_score
                    current_continue_days = user_info.continue_days
                    days = self._delt_days(str(dead_line))  # 剩余天数
                    if days <= 0:
                        continue
                    if target_type == TargetType.Rank:
                        pass
                    elif target_type == TargetType.ProblemSolve:
                        delt = target_value - current_problem_solve
                        avg = ceil(delt / days)
                        if avg >= 3:
                            msg = "亲～，您有一个刷题目标需要完成，您当前的刷题数量为: {}， 目标值为: {}，剩余" \
                                "天数为: {}，您至少每天需要完成: {} 题才能达成目标！！加油，奥利给！！".format(current_problem_solve,
                                                                                 target_value, days, avg)
                            email_service.EmailService.send_email(
                                email_addr, msg)
                    elif target_type == TargetType.CodeSubmit:
                        pass
                    elif target_type == TargetType.ProblemSubmit:
                        pass
                    elif target_type == TargetType.ContinueDays:
                        pass
                    elif target_type == TargetType.Rating:
                        pass
                    elif target_type == TargetType.Challenge:
                        pass

    def judge_rank_target(self, user, target_value, dead_line):
        pass

    def judge_problem_solve_target(self, user, target_value, dead_line):
        info = self.daoDailyInfo.search_user_recent_info(user)
        if target_value <= info.total_solve:
            return TargetStatus.SUCC
        if info.date_time >= dead_line:
            return TargetStatus.FAIL
        return TargetStatus.PROCESSING

    def judge_code_submit_target(self, user, target_value, dead_line):
        info = self.daoDailyInfo.search_user_recent_info(user)
        if target_value <= info.code_submit:
            return TargetStatus.SUCC
        if info.date_time >= dead_line:
            return TargetStatus.FAIL
        return TargetStatus.PROCESSING

    def judge_problem_submit_target(self, user, target_value, dead_line):
        info = self.daoDailyInfo.search_user_recent_info(user)
        if target_value <= info.problem_submit:
            return TargetStatus.SUCC
        if info.date_time >= dead_line:
            return TargetStatus.FAIL
        return TargetStatus.PROCESSING

    def judge_continue_days_target(self, user, target_value, dead_line):
        info = self.daoDailyInfo.search_user_recent_info(user)
        if target_value <= info.continue_days:  # 如果目标值比当前值小则成功
            return TargetStatus.SUCC
        if info.date_time >= dead_line:  # 如果当前日期大于deadline则失败
            return TargetStatus.FAIL
        return TargetStatus.PROCESSING

    def judge_rating_target(self, user, target_value, dead_line):
        info = self.daoDailyInfo.search_user_recent_info(user)
        if target_value <= info.rating_score:
            return TargetStatus.SUCC
        if info.date_time >= dead_line:
            return TargetStatus.FAIL
        return TargetStatus.PROCESSING

    def judge_challenge_target(self, user, opponent, dead_line):
        you = self.daoDailyInfo.search_user_recent_info(user)
        other = self.daoDailyInfo.search_user_recent_info(
            opponent)
        if you.date_time == dead_line and you.rating_score > other.rating_score:
            return TargetStatus.SUCC
        if you.date_time > dead_line:
            return TargetStatus.FAIL
        return TargetStatus.PROCESSING

    def get_user_unfinished_targets(self, user):
        return self.daoTarget.load_single_user_unfinished_target_info(user)

    def add_user_target(self, info):
        return self.daoTarget.add_user_target(info)

    def deal_all_targets_status_before_day(self, day):
        target_infos = self.daoTarget.get_all_targets_befor_day(day)
        user_coins = {}
        for target in target_infos:
            id = target.id
            user = target.user
            # if user != 'smilecode-2':  # 调试代码
            #     continue
            target_type = target.target_type
            target_value = target.target_value
            opponent = target.opponent
            status = target.status
            dead_line = target.dead_line
            level = target.level
            if user not in user_coins:
                user_coins[user] = 0
            if opponent != '' and opponent not in user_coins:
                user_coins[opponent] = 0
            if target_type == TargetType.Rank:
                pass
            elif target_type == TargetType.ProblemSolve:
                status = self.judge_problem_solve_target(
                    user, target_value, dead_line)
            elif target_type == TargetType.CodeSubmit:
                status = self.judge_code_submit_target(
                    user, target_value, dead_line)
            elif target_type == TargetType.ProblemSubmit:
                status = self.judge_problem_submit_target(
                    user, target_value, dead_line)
            elif target_type == TargetType.ContinueDays:
                status = self.judge_continue_days_target(
                    user, target_value, dead_line)
            elif target_type == TargetType.Rating:
                status = self.judge_rating_target(
                    user, target_value, dead_line)
            elif target_type == TargetType.Challenge:
                status = self.judge_challenge_target(user, opponent, dead_line)
            if status == TargetStatus.SUCC:
                logger.info(
                    "{} finished target_type {} successful!".format(user, target))
            elif status == TargetStatus.FAIL:
                logger.info("{} target_type {} failed!".format(user, target))
            self.daoTarget.update_user_target_status(id, status)

            if status == TargetStatus.SUCC:
                user_coins[user] = TargetLevel.from_level_to_score(level)
                if target_type == TargetType.Challenge:
                    user_coins[opponent] = floor(
                        -TargetLevel.from_level_to_score(level) / 2)
            elif status == TargetStatus.FAIL:
                user_coins[user] = floor(
                    -TargetLevel.from_level_to_score(level) / 2)
                if target_type == TargetType.Challenge:
                    user_coins[opponent] = TargetLevel.from_level_to_score(
                        level)
        for user in user_coins:
            his_coins = self.daoAccount.search_user_coins(user)
            if not his_coins:
                continue
            his_coins += user_coins[user]
            self.daoAccount.update_user_coins(user, his_coins)


if __name__ == '__main__':
    import game_play
    user = 'smilecode-2'
    target_type = 2
    target_val = 970
    opponent = "CNLYJ"
    dead_line = '2023-02-28'
    gameplay = game_play.GamePlay()
    obj = TargetService(gameplay)
    obj.deal_all_targets_status_before_day(dead_line)

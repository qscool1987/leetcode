"""
用户自定义目标
"""
from math import ceil, floor
import mysql_service
from loghandle import logger
import datetime
from dateutil.parser import parse
from lc_error import ErrorCode
import math
import email_service
from loghandle import logger


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
    def __init__(self, sql_service, game_play):
        self.sql_service = sql_service
        self.game_play = game_play

    def _deal_challenge_target(self, you, opponent, dead_line):
        you_info = self.sql_service.search_account(you)
        opponent_info = self.sql_service.search_account(opponent)
        you_email = you_info[4]
        opponent_email = opponent_info[4]
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
        nowinfo = self.sql_service.search_user_recent_info(user)
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

    def evaluate_problem_solve_target_level(self, nowinfo, target_val, dead_line):
        if nowinfo[1] >= target_val:  # 目标不合理
            return ErrorCode.PROBLEM_NUM_OVER, 0
        diff_val = target_val - nowinfo[1]
        delt_days = self._delt_days(dead_line)
        avg = diff_val / delt_days
        avg = floor(avg)
        level = 0
        if avg == 0:
            return ErrorCode.AVG_PROBLEM_NUM_SMALL, level
        elif avg == 1:
            level = TargetLevel.VERY_EASY
        elif avg == 2:
            level = TargetLevel.EASY
        elif avg == 3:
            level = TargetLevel.MID
        elif avg == 4:
            level = TargetLevel.LITTLE_HARD
        elif avg == 5:
            level = TargetLevel.HARD
        elif avg == 6:
            level = TargetLevel.VERY_HARD
        else:
            level = TargetLevel.UNBELIEVABLE
        return ErrorCode.SUCC, level

    def evaluate_code_submit_target_level(self, nowinfo, target_val, dead_line):
        if nowinfo[2] >= target_val:
            return ErrorCode.CODELINE_OVER, 0
        diff_val = target_val - nowinfo[2]
        delt_days = self._delt_days(dead_line)
        avg = diff_val / delt_days
        avg = floor(avg)
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
        if nowinfo[3] >= target_val:  # 目标不合理
            return ErrorCode.PROBLEM_SUBMIT_OVER, 0
        diff_val = target_val - nowinfo[3]
        delt_days = self._delt_days(dead_line)
        avg = 3 * diff_val / delt_days
        avg = floor(avg)
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
        if nowinfo[4] >= target_val:  # 目标不合理
            return ErrorCode.RATING_OVER, 0
        if nowinfo[4] == 0:
            return ErrorCode.NO_RATING_SCORE, 0
        diff_val = target_val - nowinfo[4]
        if diff_val < 50:
            return ErrorCode.RATING_GAP_SMALL, 0
        delt_days = self._delt_days(dead_line)
        if delt_days < 30:
            return ErrorCode.DATETIME_GAP_SHORT, 0
        nowscore = nowinfo[4]
        pvar = self._cal_rating_param(nowscore, target_val)
        level = self._cal_rating_target_level(diff_val, delt_days, pvar)
        return ErrorCode.SUCC, level

    def evaluate_challenge_target_level(self, you, oponent, dead_line):
        other = self.sql_service.search_user_recent_info(oponent)
        if not other:
            return ErrorCode.OPPNENT_NOT_EXIST, 0
        if you[4] == 0:
            return ErrorCode.NO_RATING_SCORE, 0
        if you[4] >= other[4]:
            return ErrorCode.PK_RATING_OVER, 0
        diff_val = other[4] - you[4]
        delt_days = self._delt_days(dead_line)
        if delt_days < 30:
            return ErrorCode.DATETIME_GAP_SHORT, 0
        pvar = 1
        nowscore = you[4]
        target_val = other[4]
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
        self._deal_challenge_target(you[0], other[0], dead_line)
        return ErrorCode.SUCC, level

    def deal_all_targets_status(self):
        target_infos = self.sql_service.load_all_unfinished_target_info()
        for target in target_infos:
            id = target[0]
            user = target[1]
            target_type = target[2]
            target_value = target[3]
            opponent = target[4]
            status = target[5]
            dead_line = target[7]
            level = target[8]
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
            self.sql_service.update_user_target_status(id, status)
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

    def judge_rank_target(self, user, target_value, dead_line):
        pass

    def judge_problem_solve_target(self, user, target_value, dead_line):
        info = self.sql_service.search_user_recent_info(user)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[1]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_code_submit_target(self, user, target_value, dead_line):
        info = self.sql_service.search_user_recent_info(user)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[2]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_problem_submit_target(self, user, target_value, dead_line):
        info = self.sql_service.search_user_recent_info(user)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[3]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_continue_days_target(self, user, target_value, dead_line):
        info = self.sql_service.search_user_recent_info(user)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[5]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_rating_target(self, user, target_value, dead_line):
        info = self.sql_service.search_user_recent_info(user)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[4]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_challenge_target(self, user, opponent, dead_line):
        you = self.sql_service.search_user_recent_info(user)
        other = self.sql_service.search_user_recent_info(
            opponent)
        if you[-1] > dead_line:
            return TargetStatus.FAIL
        if you[4] > other[4]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING


if __name__ == '__main__':
    import game_play
    user = 'smilecode-2'
    target_type = 7
    target_val = 1800
    opponent = "CNLYJ"
    dead_line = '2022-12-31'
    sql_service = mysql_service.MysqlService()
    gameplay = game_play.GamePlay()
    obj = TargetService(sql_service, gameplay)
    obj._deal_challenge_target(user, opponent, dead_line)
    # obj.deal_all_targets_status()
    # target_infos = sql_service.load_all_unfinished_target_info2()
    # for target in target_infos:
    #     id = target[0]
    #     user = target[1]
    #     target_type = target[2]
    #     target_value = target[3]
    #     opponent = target[4]
    #     status = target[5]
    #     dead_line = str(target[7])
    #     level = target[8]
    #     if target_type != TargetType.Challenge:
    #         errcode, level = obj.evaluate_target_level(
    #             user, target_type, target_val=target_value, dead_line=dead_line)
    #     else:
    #         errcode, level = obj.evaluate_target_level(
    #             user, target_type, target_val=target_value, opponent=opponent, dead_line=dead_line)
    #     print(errcode, level)
    #     if errcode != 0:
    #         sql_service.update_user_target_level(id, 1)
    #     else:
    #         sql_service.update_user_target_level(id, level)
    # errcode, level = obj.evaluate_target_level(
    #     user, target_type, target_val, opponent=opponent, dead_line=dead_line)
    # print(errcode, level)

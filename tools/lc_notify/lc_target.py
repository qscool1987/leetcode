"""
用户自定义目标
"""
from math import ceil, floor
import mysql_service
from loghandle import logger
import datetime
from dateutil.parser import parse
from lc_error import ErrorCode


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
        avg = ceil(avg)
        level = 0
        if avg <= 1:
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
        avg = ceil(avg)
        level = 0
        if avg <= 20:
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
        avg = ceil(avg)
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

    def evaluate_rating_target_level(self, nowinfo, target_val, dead_line):
        if nowinfo[4] >= target_val:  # 目标不合理
            return ErrorCode.RATING_OVER, 0
        if nowinfo[4] == 0:
            return ErrorCode.NO_RATING_SCORE, 0
        diff_val = target_val - nowinfo[4]
        if diff_val < 50:
            return ErrorCode.RATING_GAP_SMALL, 0
        delt_days = self._delt_days(dead_line)
        if delt_days < 30:
            return ErrorCode.DATETIME_GAP_SHORT
        avg = 7 * diff_val / delt_days  # 每周
        avg = ceil(avg)
        level = 0
        if avg <= 10:
            level = TargetLevel.VERY_EASY
        elif avg > 10 and avg <= 15:
            level = TargetLevel.EASY
        elif avg > 15 and avg <= 20:
            level = TargetLevel.MID
        elif avg > 20 and avg <= 25:
            level = TargetLevel.LITTLE_HARD
        elif avg > 25 and avg <= 30:
            level = TargetLevel.HARD
        elif avg > 30 and avg <= 35:
            level = TargetLevel.VERY_HARD
        else:
            level = TargetLevel.UNBELIEVABLE
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
        avg = 7 * diff_val / delt_days
        level = 0
        if avg <= 20:
            level = TargetLevel.VERY_EASY
        elif avg > 20 and avg <= 25:
            level = TargetLevel.EASY
        elif avg > 25 and avg <= 30:
            level = TargetLevel.MID
        elif avg > 30 and avg <= 35:
            level = TargetLevel.LITTLE_HARD
        elif avg > 35 and avg <= 40:
            level = TargetLevel.HARD
        elif avg > 40 and avg <= 45:
            level = TargetLevel.VERY_HARD
        else:
            level = TargetLevel.UNBELIEVABLE
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
            if status == TargetStatus.SUCC:  # 根据目标等级 * 5
                self.game_play.add_user_coins(
                    user, TargetLevel.from_level_to_score(level))
            elif status == TargetStatus.FAIL:  # 目标失败扣10分
                self.game_play.add_user_coins(user, -10)

    def judge_rank_target(self, user, target_value, dead_line):
        pass

    def judge_problem_solve_target(self, user, target_value, dead_line):
        today = datetime.date.today()
        info = self.sql_service.search_user_recent_info(user)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[1]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_code_submit_target(self, user, target_value, dead_line):
        today = datetime.date.today()
        info = self.sql_service.search_user_recent_info(user)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[2]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_problem_submit_target(self, user, target_value, dead_line):
        today = datetime.date.today()
        info = self.sql_service.search_user_recent_info(user)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[3]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_continue_days_target(self, user, target_value, dead_line):
        today = datetime.date.today()
        info = self.sql_service.search_user_recent_info(user)
        print(info, user)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[5]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_rating_target(self, user, target_value, dead_line):
        today = datetime.date.today()
        info = self.sql_service.search_user_recent_info(user)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[4]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_challenge_target(self, user, opponent, dead_line):
        today = datetime.date.today()
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
    # user = 'smilecode-2'
    # target_type = 7
    # target_val = "ou-hai-zijhu23dnz"
    # dead_line = '2022-12-15'
    sql_service = mysql_service.MysqlService()
    gameplay = game_play.GamePlay()
    obj = TargetService(sql_service, gameplay)
    # obj.deal_all_targets_status()
    target_infos = sql_service.load_all_unfinished_target_info2()
    for target in target_infos:
        id = target[0]
        user = target[1]
        target_type = target[2]
        target_value = target[3]
        opponent = target[4]
        status = target[5]
        dead_line = str(target[7])
        level = target[8]
        if target_type != TargetType.Challenge:
            errcode, level = obj.evaluate_target_level(
                user, target_type, target_val=target_value, dead_line=dead_line)
        else:
            errcode, level = obj.evaluate_target_level(
                user, target_type, target_val=target_value, opponent=opponent, dead_line=dead_line)
        print(errcode, level)
        if errcode != 0:
            sql_service.update_user_target_level(id, 1)
        else:
            sql_service.update_user_target_level(id, level)

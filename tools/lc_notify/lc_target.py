"""
用户自定义目标
"""
import mysql_service
import lc_service
from loghandle import logger
import datetime


class TargetType:
    Rank = 1  # 周赛排名
    ProblemSolve = 2  # 总刷题量
    CodeSubmit = 3  # push代码行数
    ProblemSubmit = 4  # push题目数量
    ContinueDays = 5  # 连续打卡天数
    Rating = 6  # 竞赛分数
    Challenge = 7  # 挑战pk

    def from_type_to_str(self, target_type):
        if target_type == self.Rank:
            return "周赛排名"
        elif target_type == self.ProblemSolve:
            return "总刷题量"
        elif target_type == self.CodeSubmit:
            return "push代码行数"
        elif target_type == self.ProblemSubmit:
            return "push代码题量"
        elif target_type == self.ContinueDays:
            return "连续打卡天数"
        elif target_type == self.Rating:
            return "竞赛分数"
        elif target_type == self.Challenge:
            return "挑战PK"
        else:
            return None

    def from_str_to_type(self, target):
        if target == "周赛排名":
            return self.Rank
        elif target == "总刷题量":
            return self.ProblemSolve
        elif target == "push代码行数":
            return self.CodeSubmit
        elif target == "push代码题量":
            return self.ProblemSubmit
        elif target == "连续打卡天数":
            return self.ContinueDays
        elif target == "竞赛分数":
            return self.Rating
        elif target == "挑战PK":
            return self.Challenge
        return 0


class TargetStatus:
    UNKNOW = 0
    PROCESSING = 1
    SUCC = 2
    FAIL = 3


class TargetService(object):
    def __init__(self):
        self.lc_service = lc_service.LeetcodeService()
        self.sql_service = mysql_service.MysqlService()
        td = datetime.date.today()
        self.today = td

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

    def judge_rank_target(self, user, target_value, dead_line):
        pass

    def judge_problem_solve_target(self, user, target_value, dead_line):
        info = self.sql_service.serach_single_user_daily_info(user, self.today)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[1]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_code_submit_target(self, user, target_value, dead_line):
        info = self.sql_service.serach_single_user_daily_info(user, self.today)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[2]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_problem_submit_target(self, user, target_value, dead_line):
        info = self.sql_service.serach_single_user_daily_info(user, self.today)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[3]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_continue_days_target(self, user, target_value, dead_line):
        info = self.sql_service.serach_single_user_daily_info(user, self.today)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[5]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_rating_target(self, user, target_value, dead_line):
        info = self.sql_service.serach_single_user_daily_info(user, self.today)
        if info[-1] > dead_line:
            return TargetStatus.FAIL
        if target_value <= info[4]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING

    def judge_challenge_target(self, user, opponent, dead_line):
        you = self.sql_service.serach_single_user_daily_info(user, self.today)
        other = self.sql_service.serach_single_user_daily_info(
            opponent, self.today)
        if you[-1] > dead_line:
            return TargetStatus.FAIL
        if you[4] > other[4]:
            return TargetStatus.SUCC
        return TargetStatus.PROCESSING


if __name__ == '__main__':
    obj = TargetService()
    obj.deal_all_targets_status()

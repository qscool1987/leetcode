#coding=utf-8
#!/usr/bin/env python
import json
import requests
import datetime
import settings
from lc_git_stat import (stat_git_info, git_pull)
from loghandle import logger
import mysql_service
import email_service
import lc_service
import sys

user_list2 = ['smilecode-2'] #用于调试

# 数据库服务对象
sql_service = mysql_service.MysqlService()

# 访问leetcode官方接口的对象
leetcode_service = lc_service.LeetcodeService()

def stat_user_info():
    """
    统计所有用户的刷题信息并进行汇总，和昨日信息进行对比，将结果记录到mysql
    如果有用户触发奖励条件，则给用户发送邮件通知
    """
    # 更新本地git代码库，后面统计代码贡献
    git_pull()
    td = datetime.date.today()
    yd = td + datetime.timedelta(days = -1)
    td_infos = {}
    user_score = {}
    git_infos = {}
    td = str(td)
    yd = str(yd)
    # 从数据库加载昨天的统计信息, 账户映射信息, 奖牌信息
    yd_infos = sql_service.load_all_user_daily_info_by_day(yd)
    lc_to_git, medal_history, user_award, user_email = sql_service.load_account_info()
    user_list = []
    for u in medal_history:
        user_list.append(u)
    td_medals = {}
    for u in user_list:
        # 获取刷题信息
        res = leetcode_service.get_user_lc_stat_info(u)
        td_infos[u] = res
        # 获取竞赛分数信息
        score = leetcode_service.get_user_score_info(u)
        user_score[u] = score
        # 获取奖牌信息
        cur_medal = leetcode_service.get_user_medal_info(u)
        td_medals[u] = cur_medal
        # 获取git代码贡献信息
        if u in lc_to_git:
            git_info = stat_git_info(td, lc_to_git[u])
            git_infos[u] = git_info
    user_award_info = {}
    # 处理medal
    for u in td_medals:
        if u not in medal_history:
            sql_service.add_account_info(u, '', td_medals[u])
        else:
            history = int(medal_history[u])
            user_award_info[u] = [history, 0]
            # 对比历史，如果比历史成绩好则更新
            if (history & td_medals[u]) == 0:
                history += td_medals[u] 
                user_award_info[u] = [history, td_medals[u]]  
    # 对比
    result = []
    hour = datetime.datetime.now().hour
    for u in user_list:
        y_l = []
        if u in yd_infos:
            y_l = yd_infos[u]
        t_l = []
        if u in td_infos:
            t_l = td_infos[u]
        else:
            continue
        if u in lc_to_git:
            ln, lt = git_infos[u]
            t_l[2] = ln
            t_l[3] = lt
        if u in user_score:
            t_l[4] = user_score[u]
        if len(y_l) == 0:
            t_l[6] = t_l[1] # 今日刷题量 新加的用户为总刷题量
            t_l[5] = 1 # 连续打卡天数 新加的用户为1
            t_l[7] = 0 # 懒惰等级 新加的用户初始化为0
        else:
            diff_t = int(t_l[1]) - int(y_l[1])
            t_l[6] = diff_t
            if diff_t > 0:
                t_l[5] += int(y_l[5]) + 1
                t_l[7] = int(y_l[7]) - 2 # 只要今日刷过题，则懒惰等级-2
                if t_l[7] < 0: # 最低不低于0
                    t_l[7] = 0
            else:
                t_l[5] = 0
                # 如果今天晚上23点后统计还是没有刷题，则懒懒等级+1
                if hour >= 23:
                    t_l[7] = int(y_l[7]) + 1
                else:
                    t_l[7] = int(y_l[7])
        if t_l[2] >= 1000 and (user_award_info[u][0] & settings.MedalType.CodeSubmit) == 0:
            user_award_info[u][0] += settings.MedalType.CodeSubmit
            user_award_info[u][1] = settings.MedalType.CodeSubmit
        if t_l[3] >= 50 and (user_award_info[u][0] & settings.MedalType.ProblemSubmit) == 0:
            user_award_info[u][0] += settings.MedalType.ProblemSubmit
            user_award_info[u][1] = settings.MedalType.ProblemSubmit
        if t_l[5] >= 100 and (user_award_info[u][0] & settings.MedalType.ContinueDays) == 0:
            user_award_info[u][0] += settings.MedalType.ContinueDays
            user_award_info[u][1] = settings.MedalType.ContinueDays
        result.append(t_l)
    logger.info(result)

    # # 将今日统计信息写入数据库
    # for item in result:
    #     user = item[0]
    #     info = sql_service.serach_single_user_daily_info(user, td)
    #     if not info:
    #         sql_service.add_single_user_daily_info(td, item)
    #     else:
    #         sql_service.update_single_user_daily_info(td, item)
    # logger.info("add into mysql finished")
    # # 发送邮件
    # emailobj = email_service.EmailService(user_email)
    # for u in user_award_info:
    #     if user_award[u] == 0 and user_award_info[u][1] > 0:
    #         emailobj.send_email(u, user_award_info[u][1], True)
    #         sql_service.update_user_award(u, 1)
    #         logger.info("send email to {} for award congratuation".format(u))
    #     elif user_award_info[u][1] > 0 and (medal_history[u] & user_award_info[u][1]) == 0:
    #         emailobj.send_email(u, user_award_info[u][1], False)
    #         logger.info("send email to {} for stage congratuation".format(u))
    #     sql_service.update_user_medal(u, user_award_info[u][0])


if __name__ == '__main__':
    stat_user_info()

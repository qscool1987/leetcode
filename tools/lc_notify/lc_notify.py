#coding=utf-8
#!/usr/bin/env python
import csv
import os
import sys
import numpy as np
import pandas as pd
import json
import requests
import datetime
import xlwt
import xlrd
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
import settings
from lc_git_stat import stat_git_info
from loghandle import logger
import mysql_service

user_list2 = ['smilecode-2'] #用于调试

# 数据库服务对象
sql_service = mysql_service.mysqlService()  

def get_user_medal_info(user):
    """获取用户当前的奖牌信息"""
    url = 'https://leetcode.cn/graphql/noj-go/'
    headers = {
        "content-type": "application/json",
    }
    data = {
        "query":"\n    query contestBadge($userSlug: String!) {\n  userProfileUserLevelMedal(userSlug: $userSlug) {\n    current {\n      name\n      obtainDate\n      category\n      config {\n        icon\n        iconGif\n        iconGifBackground\n      }\n      id\n      year\n      month\n      hoverText\n    }\n    next {\n      name\n      obtainDate\n      category\n      config {\n        icon\n        iconGif\n        iconGifBackground\n      }\n      id\n      year\n      month\n      hoverText\n      everOwned\n    }\n  }\n}\n    ",
         "variables":{"userSlug":user}
    }
    res = requests.post(url, data=json.dumps(data), headers=headers).json()['data']['userProfileUserLevelMedal']['current']
    if res:
        if res['name'] == 'Knight':
            return 1
        elif res['name'] == 'Guardian':
            return 2
    return 0

def get_user_score_info(user):
    """获取用户当前的分数信息"""
    url = 'https://leetcode.cn/graphql/noj-go/'
    headers = {
        "content-type": "application/json",
    }
    data = {
        "query": "query userContestRankingInfo($userSlug: String!) {\n  userContestRanking(userSlug: $userSlug) {\n    attendedContestsCount\n    rating\n    globalRanking\n    localRanking\n    globalTotalParticipants\n    localTotalParticipants\n    topPercentage\n  }\n  userContestRankingHistory(userSlug: $userSlug) {\n    attended\n    totalProblems\n    trendingDirection\n    finishTimeInSeconds\n    rating\n    score\n    ranking\n    contest {\n      title\n      titleCn\n      startTime\n    }\n  }\n}\n    ",
        "variables": {
            "userSlug": user
        }
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    data = res.json().get('data')
    if not data:
        return 0
    data = data.get('userContestRanking')
    if not data:
        return 0
    score = data.get('rating')
    if not score:
        return 0
    return int(score)

def get_user_lc_stat_info(user):
    """获取用户当前的刷题信息"""
    url = 'https://leetcode.cn/graphql/noj-go/'
    headers = {
        "content-type": "application/json",
    }
    data = {
        "query": "\n    query languageStats($userSlug: String!) {\n  userLanguageProblemCount(userSlug: $userSlug) {\n    languageName\n    problemsSolved\n  }\n}\n    ",
        "variables" : {
            "userSlug": user
        }
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    data = res.json()['data']['userLanguageProblemCount']
    t_langinfo = {}
    for item in data: 
        t_langinfo[item['languageName']] = item['problemsSolved']
    t_total = 0
    line = [user, 0, 0, 0, 0, 0, 0]
    for lang in settings.languages:
        t_cnt = 0
        if lang in t_langinfo:
            t_cnt = t_langinfo[lang]
        t_total += t_cnt
    line[1] = str(t_total)
    return line

def stat_user_info():
    """
    统计所有用户的刷题信息并进行汇总，生成excel表，并对提供邮箱的用户发送邮件，excel作为邮件附件发送
    """
    td = datetime.date.today()
    yd = td + datetime.timedelta(days = -1)
    td_infos = {}
    user_score = {}
    git_infos = {}
    td = str(td)
    yd = str(yd)
    # 从数据库加载昨天的统计信息, 账户映射信息, 奖牌信息
    yd_infos = sql_service.load_user_daily_info(yd)
    lc_to_git, medal_history = sql_service.load_account_info()
    user_list = []
    for u in medal_history:
        user_list.append(u)
    td_medals = {}
    for u in user_list:
        # 获取刷题信息
        res = get_user_lc_stat_info(u)
        td_infos[u] = res
        # 获取竞赛分数信息
        score = get_user_score_info(u)
        user_score[u] = score
        # 获取奖牌信息
        cur_medal = get_user_medal_info(u)
        td_medals[u] = cur_medal
        # 获取git代码贡献信息
        if u in lc_to_git:
            git_info = stat_git_info(td, lc_to_git[u])
            git_infos[u] = git_info
    # 处理medal
    for u in td_medals:
        if u not in medal_history:
            sql_service.add_account_info(u, '', td_medals[u])
        else:
            history = int(medal_history[u])
            if history < td_medals[u]:
                sql_service.update_user_medal(u, td_medals[u])
    # 对比
    result = []
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
            t_l[6] = t_l[1]
            t_l[5] = 1
        else:
            diff_t = int(t_l[1]) - int(y_l[1])
            t_l[6] = diff_t
            if diff_t > 0:
                t_l[5] += int(y_l[5]) + 1
            else:
                t_l[5] = 0
        result.append(t_l)
    logger.info(result)

    # 将今日统计信息写入数据库
    sql_service.add_user_daily_info(td, result)
    logger.info("add into mysql finished")


if __name__ == '__main__':
    stat_user_info()

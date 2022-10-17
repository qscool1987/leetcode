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

def load_lc_stat_inf_from_excel(filepath):
    """
    已经不在从excel中读取前一天的数据, 该函数不在使用
    """
    wb = xlrd.open_workbook(filepath)
    sheet = wb.sheets()[0]
    row_n = sheet.nrows
    col_n = sheet.ncols
    res = {}
    for i in range(0, row_n):
        if i == 0:
            continue
        info = []
        for j in range(0, col_n):
            info.append(sheet.cell_value(i,j))
        if info[0] == '-':
            continue
        for k in range(1, len(info)):
            info[k] = int(info[k])
        res[info[0]] = info
    return res

def send_email(user, file_path, dt, medal_history):
    """
    user: 待接受邮件的用户
    file_path: 邮件的附件文件路径
    dt: 日期，用于附件的文件名
    注意: 暂时采用发邮件的方式通知用户, 当网站搭建完毕后将弃用
    """
    to_addr = settings.emails[user]
    fm_addr = '595949643@qq.com'
    pass_wd = 'zeichyzgngnlbche'
    ret = True
    try:
        msg = MIMEMultipart()
        cur_medal = get_user_medal_info(user)
        if medal_history[user] == 0 and cur_medal == 1:
            sql_service.update_user_medal(user, cur_medal)
            msg.attach(MIMEText('恭喜你，上Knight了!', 'plain', 'utf-8'))
        elif medal_history[user] <= 1 and cur_medal == 2:
            sql_service.update_user_medal(user, cur_medal)
            msg.attach(MIMEText('恭喜你，上Guardian了!', 'plain', 'utf-8'))
        medal_history[user] = cur_medal
        msg.attach(MIMEText('请注意！您今天忘记刷题了吗。。。亲～', 'plain', 'utf-8'))
        msg['Subject'] = "leetcode刷题通知！"
        msg['From'] = fm_addr
        msg['To'] = to_addr
        # 构造附件
        filename = 'leetcode_' + dt + '.xls'
        att = MIMEText(open(file_path, 'rb').read(), 'base64', 'gb2312')
        att["Content-Type"] = 'application/octet-stream'
        att.add_header("Content-Disposition", 'attachment', filename=filename)
        msg.attach(att)
        # 创建 SMTP 对象
        smtp = smtplib.SMTP_SSL("smtp.qq.com")
        # 登录，需要：登录邮箱和授权码
        smtp.login(user=fm_addr, password=pass_wd)
        smtp.sendmail(fm_addr, to_addr, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        smtp.quit()  # 关闭连接
    except Exception as e:  
        logger.error(e)
        ret = False
    return ret

def stat_user_info():
    """
    统计所有用户的刷题信息并进行汇总，生成excel表，并对提供邮箱的用户发送邮件，excel作为邮件附件发送
    """
    td_infos = {}
    td = datetime.date.today()
    user_score = {}
    git_infos = stat_git_info(td)
    for u in settings.user_list:
        res = get_user_lc_stat_info(u)
        score = get_user_score_info(u)
        user_score[u] = score
        td_infos[u] = res
    yd = td + datetime.timedelta(days = -1)
    td = str(td)
    yd = str(yd)
    # 从数据库加载昨天的统计信息, 账户映射信息, 奖牌信息
    yd_infos = sql_service.load_user_daily_info(yd)
    lc_to_git, medal_history = sql_service.load_account_info()

    # 对比
    result = []
    for u in settings.user_list:
        y_l = []
        if u in yd_infos:
            y_l = yd_infos[u]
        t_l = []
        if u in td_infos:
            t_l = td_infos[u]
        else:
            continue
        if u in lc_to_git:
            git_u = lc_to_git[u]
            ln, lt = git_infos[git_u]
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
    # 将今日统计信息进行保存
    savepath = "./data/" + td + ".xls"
    save_to_excel(result, savepath)
    # 将今日统计信息写入数据库
    sql_service.add_user_daily_info(td, result)

    # 发送邮件
    for u in settings.user_list2:
        if u in settings.emails:
            if not send_email(u, savepath, td, medal_history):
                logger.warning("{} email send fail".format(u))
    logger.info("email send finished")

def save_to_excel(result, savepath):
    """
    将result的内容写入到savepath文件中，存储为.xls格式
    result: 写入到excel表的内容
    savepath: excel表的文件名
    """
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet('leetcode',cell_overwrite_ok=True)
    columns = settings.excel_cols
    for i in range(0, len(columns)):
        sheet.write(0, i, columns[i])
    for i in range(0, len(result)+1):
        if i == len(result):
            for j in range(0, len(columns)):
                sheet.write(i+1, j, '-')
            break
        data = result[i]
        for j in range(0, len(columns)):
            sheet.write(i+1,j,data[j])
    book.save(savepath)


if __name__ == '__main__':
    stat_user_info()

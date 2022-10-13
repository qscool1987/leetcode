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
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart


user_list = ['zerotrac2','smilecode-2', 'aween', 'zzz-4t8', 'ChinaYC', 'CNLYJ', 'linuxer',
            'slluosali', 'Vergissmeinncht', 'daydayup', 'flippedli-xiao-hua', 
            'caicodehh', 'cardioid-t', 'ou-hai-zijhu23dnz',
            'exciting-tesla7ck', 'lao-qi-e-r']
user_list2 = ['CNLYJ'] #用于调试

# no_email_users = [
#     'linuxer',
#     'cardioid-t', 
#     'exciting-tesla7ck'
#     ]

languages = ['C++', 'Java', 'Python3', 'MySQL', 'Ruby', 'Bash', 'Go']

emails = {
    'caicodehh': '1748493969@qq.com',
    'flippedli-xiao-hua': 'lizhenhua0202@163.com',
    'smilecode-2': '595949643@qq.com',
    'CNLYJ': '1910198192@qq.com',
    'zzz-4t8': '1192963064@qq.com',
    'aween': '376087731@qq.com',
    'lao-qi-e-r': '2460762414@qq.com',
    'slluosali': '1554548256@qq.com',
    'daydayup': 'jiangwr1996@163.com',
    'Vergissmeinncht': '1936800723@qq.com',
    'ChinaYC': 'liuyichaochina@gmail.com',
    'ou-hai-zijhu23dnz': '196082511@qq.com'
    }

def get_user_medal_info(user):
    """获取用户当前的分数信息"""
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
    return res.json()

def get_user_info(user):
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
    return res.json()


def send_email(user, file_path, dt, medal_history):
    """
    user: 待接受邮件的用户
    file_path: 邮件的附件文件路径
    dt: 日期，用于附件的文件名
    """
    to_addr = emails[user]
    fm_addr = '595949643@qq.com'
    pass_wd = 'zeichyzgngnlbche'
    ret = True
    try:
        msg = MIMEMultipart()
        cur_medal = get_user_medal_info(user)
        if medal_history == 0 and cur_medal == 1:
            msg.attach(MIMEText('恭喜你，上Knight了!', 'plain', 'utf-8'))
        elif medal_history <= 1 and cur_medal == 2:
            msg.attach(MIMEText('恭喜你，上Guardian了!', 'plain', 'utf-8'))
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
        print(e)
        ret = False
    return ret
#  res.json()
def stat_user_info():
    """
    统计所有用户的刷题信息并进行汇总，生成excel表，并对提供邮箱的用户发送邮件，excel作为邮件附件发送
    """
    td_infos = {}
    td = datetime.date.today()
    for u in user_list:
        res = get_user_info(u)
        # score = get_user_score_info(u)
        td_infos[u] = res['data']['userLanguageProblemCount']

    filepath = "./data/" + str(td) + '.xls'
    with open(filepath, 'w') as fp:
        fp.write(json.dumps(td_infos))
    
    yd = td + datetime.timedelta(days = -1)
    filepath  = "./data/" + str(yd)
    yd_infos = {}
    medal_file_path = "./data/medal.csv"
    medal_history = {}
    if not os.path.exists(medal_file_path):
        for u in user_list:
            medal_history[u] = get_user_medal_info(u)
        medal_history_pd = pd.DataFrame(medal_history, index=['medal']).T
        medal_history_pd.to_csv(medal_file_path)
    else:
        medal_history_pd = pd.read_csv(medal_file_path)
        for _, user_medal in medal_history_pd.iterrows():
            medal_history[user_medal[0]] = user_medal[1]

    if not os.path.exists(filepath):
        print("error: yesterday stat info not exists")
    else:
        with open(filepath) as fp:
            data = fp.read()
            yd_infos = json.loads(data)
    # 对比
    td = str(td)
    yd = str(yd)
    result = []
    for u in user_list:
        line = []
        itd = []
        if u in td_infos:
            itd = td_infos[u]
        iyd = []
        if u in yd_infos:
            iyd = yd_infos[u]
        t_langinfo = {}
        for item in itd:
            t_langinfo[item['languageName']] = item['problemsSolved']
        y_langinfo = {}
        for item in iyd:
            y_langinfo[item['languageName']] = item['problemsSolved']
        t_total = 0
        y_total = 0
        for lang in languages:
            t_cnt = 0
            if lang in t_langinfo:
                t_cnt = t_langinfo[lang]
            t_total += t_cnt
            y_cnt = 0
            if lang in y_langinfo:
                y_cnt = y_langinfo[lang]
            y_total += y_cnt
            # line.append(str(t_cnt) + "<---" + str(y_cnt) + " add: " + str(t_cnt-y_cnt))
            line.append(str(t_cnt-y_cnt))
        line = [u, str(t_total) + "<--" + str(y_total)] + line
        result.append(line)
    savepath = "./result/" + td + ".xls"

    save_to_excel(result, savepath)
    # 发送邮件
    for u in user_list:
        if u in emails:
            if not send_email(u, savepath, td, medal_history[u]):
                print("{} email send fail".format(u))
    print("email send finished")


def save_to_excel(result, savepath):
    """
    将result的内容写入到savepath文件中，存储为.xls格式
    result: 写入到excel表的内容
    savepath: excel表的文件名
    """
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet('leetcode',cell_overwrite_ok=True)
    columns = ['用户', '题量'] + languages
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
        
    # savepath = "./result/" + dt + ".xls"
    book.save(savepath)
    

stat_user_info()
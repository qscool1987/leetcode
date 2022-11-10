from flask import Flask
from flask import request
import datetime
import json
import mysql_service
import lc_service
from loghandle import logger
import settings
from lc_target import TargetType

sql_service = mysql_service.MysqlService()

# 访问leetcode官方接口的对象
leetcode_service = lc_service.LeetcodeService()

app = Flask(__name__)

@app.route('/all_user_daily_info')
def get_all_user_daily_info():
    td = datetime.date.today()
    yd = td + datetime.timedelta(days=-1)
    data = sql_service.load_all_user_daily_info_by_day(str(td))
    if len(data) == 0:
        data = sql_service.load_all_user_daily_info_by_day(str(yd))
    info = []
    for u in data:
        line = {}
        tmplist = list(data[u])
        lazydays = tmplist[7]
        if lazydays >= len(settings.lazyLevels):
            tmplist[7] = settings.lazyLevels[-1]
        else:
            tmplist[7] = settings.lazyLevels[lazydays]
        for i in range(0, len(sql_service.USER_LC_DAILY_INFO_FIELDS)):
            key = sql_service.USER_LC_DAILY_INFO_FIELDS[i]
            line[key] = str(tmplist[i])
        info.append(line)
    # 按今日刷题量进行排序
    info = sorted(info, key=lambda item: int(item['new_solve']), reverse=True)
    # logger.info(info)
    return json.dumps(info)


@app.route('/user_info')
def get_user_info():
    td = datetime.date.today()
    yd = td + datetime.timedelta(days=-1)
    data = sql_service.load_all_user_daily_info_by_day(str(td))
    if len(data) == 0:
        data = sql_service.load_all_user_daily_info_by_day(str(yd))
    info = []
    for u in data:
        line = []
        tmplist = list(data[u])
        lazydays = tmplist[7]
        if lazydays >= len(settings.lazyLevels):
            tmplist[7] = settings.lazyLevels[-1]
        else:
            tmplist[7] = settings.lazyLevels[lazydays]
        for item in tmplist:
            line.append(str(item))
        info.append(line)
    # 按今日刷题量进行排序
    info = sorted(info, key=lambda item: int(item[6]), reverse=True)
    # logger.info(info)
    return json.dumps(info)


@app.route('/submit_account_info')
def submit_account_info():
    ret = ['0', "succ"]
    body = request.values
    logger.info(body)
    lc_account = body.get('lc_account')
    git_account = body.get('git_account')
    email = body.get('email_account')
    blanks = [' ', '\t', '\n']
    for c in lc_account:
        if c in blanks:
            ret[0] = '1'
            ret[1] = "leetcode 账号不存在!!!"
            return json.dumps(ret)
    if email != '' and '@' not in email:
        ret[0] = '1'
        ret[1] = "邮箱格式错误!!!"
        return json.dumps(ret)
    info = leetcode_service.get_user_lc_stat_info(lc_account)
    logger.info(info)
    if not info:
        ret[0] = '1'
        ret[1] = "leetcode 账户不存在!!!"
        return json.dumps(ret)
    userinfo = sql_service.search_account(lc_account)
    if not userinfo:
        logger.info("add lc_account: " + lc_account)
        medal = leetcode_service.get_user_medal_info(lc_account)
        if medal == 2:
            medal = 3
        sql_service.add_account_info(lc_account, git_account, email, 0, medal)
    else:
        u_email = userinfo[4]
        u_git = userinfo[1]
        if lc_account != '' and email == '' and git_account == '':
            ret[0] = '1'
            ret[1] = '账户已经存在!!!'
            return json.dumps(ret)
        if (u_email != '' and email != '') or (u_git != '' and git_account != ''):
            ret[0] = '1'
            ret[1] = '邮箱或者git账户已经存在，如要更改请联系管理员!!!'
            return json.dumps(ret)
        if u_email == '' and email != '':
            logger.info(lc_account + " update email: " + email)
            sql_service.update_user_email(lc_account, email)
        if u_git == '' and git_account != '':
            logger.info(lc_account + " update git_account: " + git_account)
            sql_service.update_user_git_account(lc_account, git_account)

    return json.dumps(ret)


@app.route('/submit_feedback_info')
def submit_feedback_info():
    td = datetime.date.today()
    td = str(td)
    ret = ['0', "succ"]
    body = request.values
    logger.info(body)
    content = body.get('msg')
    if not sql_service.add_feedback_info(td, content):
        ret[0] = 1
        ret[1] = "服务端错误"
    return json.dumps(ret)

@app.route('/submit_target_info')
def submit_target_info():
    td = datetime.date.today()
    td = str(td)
    ret = ['0', "succ"]
    body = request.values
    logger.info(body)
    lc_account = body.get('lc_account')
    target_type = body.get('target_type')
    target_val = body.get('target_val')
    dead_line = body.get('dead_line')
    td = datetime.date.today()
    td = str(td)
    if dead_line <= td:
        ret[0] = '1'
        ret[1] = "完成时间设置不合理!!"
        return json.dumps(ret)
    userinfo = sql_service.search_account(lc_account)
    if not userinfo:
        ret[0] = '1'
        ret[1] = "leetcode 账户不存在"
        return json.dumps(ret)
    obj = TargetType()
    target_type = obj.from_str_to_type(target_type)
    user_targets = sql_service.load_single_user_unfinished_target_info(lc_account)
    for item in user_targets:
        if item[2] == target_type:
            ret[0] = '1'
            ret[1] = "你已经有一个同类型未完成的目标了，请先完成它!!"
            return json.dumps(ret)
    you = sql_service.serach_single_user_daily_info(lc_account, td)
    if target_type == TargetType.ProblemSolve:
        target_val = int(target_val)
        if target_val <= you[1]:
            ret[0] = '1'
            ret[1] = '目标不合理!!!'
            return json.dumps(ret)
    elif target_type == TargetType.CodeSubmit:
        target_val = int(target_val)
        if target_val <= you[2]:
            ret[0] = '1'
            ret[1] = '目标不合理!!!'
            return json.dumps(ret)
    elif target_type == TargetType.ProblemSubmit:
        target_val = int(target_val)
        if target_val <= you[3]:
            ret[0] = '1'
            ret[1] = '目标不合理!!!'
            return json.dumps(ret)
    elif target_type == TargetType.ContinueDays:
        target_val = int(target_val)
        if target_val <= you[5]:
            ret[0] = '1'
            ret[1] = '目标不合理!!!'
            return json.dumps(ret)
    elif target_type == TargetType.Rating:
        target_val = int(target_val)
        if target_val <= you[4]:
            ret[0] = '1'
            ret[1] = '目标不合理!!!'
            return json.dumps(ret)
    elif target_type == TargetType.Challenge:
        other = sql_service.serach_single_user_daily_info(target_val, td)
        if not other:
            ret[0] = '1'
            ret[1] = '挑战的人不存在!!!'
            return json.dumps(ret)
        if you[4] >= other[4]:
            ret[0] = '1'
            ret[1] = '目标不合理!!!'
            return json.dumps(ret)
    info = [lc_account, target_type, '', '', 1, td, dead_line]
    if target_type == TargetType.Challenge:
        info[3] = str(target_val)
    else:
        info[2] = int(target_val)
    sql_service.add_user_target(info)
    return json.dumps(ret)
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=810)
    #app.run(host='127.0.0.1', port=810)

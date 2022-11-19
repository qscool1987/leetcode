from flask import Flask
from flask import request
import datetime
import json
import mysql_service
import lc_service
from loghandle import logger
import settings
from lc_target import (TargetType, TargetStatus, TargetService, TargetLevel)
from lc_error import ErrorCode
import game_play
sql_service = mysql_service.MysqlService()

# 访问leetcode官方接口的对象
leetcode_service = lc_service.LeetcodeService()
gameplay = game_play.GamePlay()
target_service = TargetService(sql_service, gameplay)

app = Flask(__name__)


@app.route('/all_user_daily_info')
def get_all_user_daily_info():
    td = datetime.date.today()
    yd = td + datetime.timedelta(days=-1)
    data = sql_service.load_all_user_daily_info_by_day(str(td))
    if len(data) == 0:
        data = sql_service.load_all_user_daily_info_by_day(str(yd))
    user_coins = sql_service.load_all_account_coins()
    info = []
    for u in data:
        line = {}
        if u in user_coins:
            line['coins'] = user_coins[u]
        else:
            line['coins'] = user_coins[0]
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
            ret[0] = ErrorCode.ACCOUNT_NOT_EXIST
            ret[1] = ErrorCode.error_message(ret[0])
            return json.dumps(ret)
    if email != '' and '@' not in email:
        ret[0] = ErrorCode.EMAIL_FORMAT_ERROR
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)
    info = leetcode_service.get_user_lc_stat_info(lc_account)
    logger.info(info)
    if not info:
        ret[0] = ErrorCode.ACCOUNT_NOT_EXIST
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)
    userinfo = sql_service.search_account(lc_account)
    if not userinfo:  # 添加新用户信息，并添加最新的统计信息
        logger.info("add lc_account: " + lc_account)
        coins = 100
        medal = leetcode_service.get_user_medal_info(lc_account)
        if medal == 1:
            coins += 30
        if medal == 2:
            medal = 3
            coins += 80
        sql_service.add_account_info(
            lc_account, git_account, email, 0, medal, coins)
        score = leetcode_service.get_user_score_info(lc_account)
        info[4] = score
        info[5] = 1
        info[6] = 0
        td = datetime.date.today()
        sql_service.add_single_user_daily_info(str(td), info)
    else:
        u_email = userinfo[4]
        u_git = userinfo[1]
        if lc_account != '' and email == '' and git_account == '':
            ret[0] = ErrorCode.ACCOUNT_EXIST
            ret[1] = ErrorCode.error_message(ret[0])
            return json.dumps(ret)
        # if (u_email != '' and email != '') or (u_git != '' and git_account != ''):
        #     ret[0] = ErrorCode.EMAIL_ACCOUNT_EXIST
        #     ret[1] = ErrorCode.error_message(ret[0])
        #     return json.dumps(ret)
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
        ret[0] = ErrorCode.SERVER_ERROR
        ret[1] = ErrorCode.error_message(ret[0])
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
    delt_days = target_service._delt_days(dead_line)
    if delt_days < 15 or delt_days > 365:
        ret[0] = ErrorCode.DATETIME_GAP_SHORT
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)
    target_type = TargetType.from_str_to_type(target_type)
    if target_type != TargetType.Challenge:
        if not target_val.isdigit():
            ret[0] = ErrorCode.VALUE_NOT_INT
            ret[1] = ErrorCode.error_message(ret[0])
            return json.dumps(ret)
        target_val = int(target_val)
    user_targets = sql_service.load_single_user_unfinished_target_info(
        lc_account)
    for item in user_targets:
        if item[2] == target_type:
            ret[0] = ErrorCode.TARGET_EXIST
            ret[1] = ErrorCode.error_message(ret[0])
            return json.dumps(ret)
    info = [lc_account, target_type, 0, '', 1, td, dead_line, 0]
    if target_type == TargetType.Challenge:
        info[3] = str(target_val)
    else:
        info[2] = int(target_val)
    errcode, level = target_service.evaluate_target_level(
        lc_account, target_type, target_val=target_val, opponent=target_val, dead_line=dead_line)
    if errcode != 0:
        ret[0] = errcode
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)
    info[-1] = level
    logger.info(info)
    sql_service.add_user_target(info)
    return json.dumps(ret)


@app.route('/get_target_info')
def get_target_info():
    ret = ['0', "succ"]
    body = request.values
    logger.info(body)
    try:
        pn = body.get('pn')
        rn = body.get('rn')
        pn = int(pn)
        rn = int(rn)
        pn = (pn - 1) * rn
        logger.info("pn={}, rn={}".format(pn, rn))
        response = sql_service.get_user_target_info(pn, rn)
        data = []
        for info in response:
            item = {}
            for i in range(0, len(sql_service.USER_ATGERT_INFO_FIELDS)):
                key = sql_service.USER_ATGERT_INFO_FIELDS[i]
                val = str(info[i])
                item[key] = val
            item['target_type'] = TargetType.from_type_to_str(
                int(item['target_type']))
            item['status'] = TargetStatus.from_status_to_str(
                int(item['status']))
            item['level'] = TargetLevel.from_level_to_str(int(item['level']))
            data.append(item)
        return json.dumps(data)
    except Exception as e:
        logger.warning(e)
    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=810)
    #app.run(host='127.0.0.1', port=810)

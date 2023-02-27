from flask import Flask
from flask import request
import datetime
import json

from target_info_dao import TargetRecord, DaoTargetInfo
from rand_problem_dao import RandProblemRecord, DaoRandProblem
from interview_problem_dao import InterviewProblemRecord, DaoInterviewProblem
from feedback_dao import FeedbackRecord, DaoFeedback
from daily_info_dao import DaoDailyInfo, UserDailyInfoRecord
from account_info_dao import AccountInfoRecord, DaoAccountInfo

import lc_service
from loghandle import logger
import settings
from lc_target import (TargetType, TargetStatus, TargetService, TargetLevel)
from lc_error import ErrorCode
import game_play

# 访问leetcode官方接口的对象
leetcode_service = lc_service.LeetcodeService()

app = Flask(__name__)


@app.route('/all_user_daily_info')
def get_all_user_daily_info():
    td = datetime.date.today()
    yd = td + datetime.timedelta(days=-1)
    daoUserDailyInfo = DaoDailyInfo()
    data = daoUserDailyInfo.load_all_user_daily_info_by_day(td)
    if not data or len(data) == 0:
        data = daoUserDailyInfo.load_all_user_daily_info_by_day(yd)
    daoAccount = DaoAccountInfo()
    user_coins = daoAccount.load_all_account_coins()
    info = []
    try:
        for u, item in data.items():
            obj = item.as_dict()
            if u in user_coins:
                obj['coins'] = user_coins[u]
                obj['honer_level'] = settings.HonerLevel.from_level_to_str(user_coins[u])
            else:
                continue
            lazydays = obj['lazy_days']
            if lazydays >= settings.LazyLevel.LEVEL16:
                obj['lazy_days'] = settings.LazyLevel.from_level_to_str(
                    settings.LazyLevel.LEVEL16)
            else:
                obj['lazy_days'] = settings.LazyLevel.from_level_to_str(lazydays)
            info.append(obj)
    except Exception as ex:
        logger.warning(ex)
    # 按今日刷题量进行排序
    info = sorted(info, key=lambda item: int(item['coins']), reverse=True)
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
    if email and '@' not in email:
        ret[0] = ErrorCode.EMAIL_FORMAT_ERROR
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)
    userDailyInfo = leetcode_service.get_user_lc_stat_info(lc_account)
    if not userDailyInfo:
        ret[0] = ErrorCode.ACCOUNT_NOT_EXIST
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)
    
    daoDailyInfo = DaoDailyInfo()
    daoAccount = DaoAccountInfo()
    userinfo = daoAccount.search_account(lc_account)
    if not userinfo:  # 添加新用户信息，并添加最新的统计信息
        logger.info("add lc_account: " + lc_account)
        item = AccountInfoRecord()
        item.coins = 100
        medal = leetcode_service.get_user_medal_info(lc_account)
        if medal == 1:
            item.coins += 30
        if medal == 2:
            medal = 3
            item.coins += 80
        item.user = lc_account
        item.git_account = git_account if git_account else ''
        item.email = email if email else ''
        item.medal = medal if medal else ''
        item.date_time = datetime.date.today()
        daoAccount.add_account_info(item)
        
        score = leetcode_service.get_user_score_info(lc_account)
        userDailyInfo.rating_score = score
        userDailyInfo.continue_days = 1
        userDailyInfo.new_solve = 0
        userDailyInfo.total_days = 1
        userDailyInfo.date_time = datetime.date.today()
        daoDailyInfo.add_single_user_daily_info(userDailyInfo)
    else:
        u_email = userinfo.email
        u_git = userinfo.git_account
        if lc_account != '' and email == '' and git_account == '':
            ret[0] = ErrorCode.ACCOUNT_EXIST
            ret[1] = ErrorCode.error_message(ret[0])
            return json.dumps(ret)
        if u_email == '' and email != '':
            logger.info(lc_account + " update email: " + email)
            daoAccount.update_user_email(lc_account, email)
        if u_git == '' and git_account != '':
            logger.info(lc_account + " update git_account: " + git_account)
            daoAccount.update_user_git_account(lc_account, git_account)

    return json.dumps(ret)


@app.route('/submit_feedback_info')
def submit_feedback_info():
    ret = ['0', "succ"]
    body = request.values
    logger.info(body)
    content = body.get('msg')
    
    dao = DaoFeedback()
    date = datetime.date.today()
    if not dao.add_feedback_info(date, content):
        ret[0] = ErrorCode.SERVER_ERROR
        ret[1] = ErrorCode.error_message(ret[0])
    return json.dumps(ret)


@app.route('/get_feedback_info')
def get_feedback_info():
    body = request.values
    logger.info(body)
    pn = body.get('pn')
    rn = body.get('rn')
    pn = int(pn)
    if pn < 1:
        pn = 1
    rn = int(rn)
    pn = (pn - 1) * rn
    logger.info("pn={}, rn={}".format(pn, rn))
    dao = DaoFeedback()
    date = datetime.date.today()
    datas = dao.load_feedback_info(pn, rn)
    result = []
    for item in datas:
        result.append(item.as_dict())
    return json.dumps(result)


@app.route('/get_rand_problem_info')
def get_rand_problem_info():
    body = request.values
    logger.info(body)
    pn = body.get('pn')
    rn = body.get('rn')
    pn = int(pn)
    if pn < 1:
        pn = 1
    rn = int(rn)
    pn = (pn - 1) * rn
    logger.info("pn={}, rn={}".format(pn, rn))
    dao = DaoRandProblem()
    datas = dao.load_rand_problem_infos(pn, rn)
    result = []
    for item in datas:
        result.append(item.as_dict())
    return json.dumps(result)


@app.route('/get_interview_problem_info')
def get_interview_problem_info():
    body = request.values
    logger.info(body)
    pn = body.get('pn')
    rn = body.get('rn')
    pt = body.get('pt')
    pn = int(pn)
    rn = int(rn)
    if not pt:
        pt = -1
    else:
        pt = int(pt)
    pn = (pn - 1) * rn
    logger.info("pn={}, rn={}".format(pn, rn))
    dao = DaoInterviewProblem()
    datas = dao.load_interview_problems(pn, rn, pt)
    result = []
    for item in datas:
        result.append(item.as_dict())
    return json.dumps(result)


@app.route('/get_interview_problem_types')
def get_interview_problem_types():
    result = DaoInterviewProblem.problem_types
    res = []
    for i in range(0, len(result)):
        res.append({"type": i, "name": result[i]})
    return json.dumps(res)


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
    try:
        if not dead_line:
            ret[0] = ErrorCode.DATETIME_GAP_SHORT
            ret[1] = ErrorCode.error_message(ret[0])
            return json.dumps(ret)
        dao_account = DaoAccountInfo()
        dao_daily = DaoDailyInfo()
        gameplay = game_play.GamePlay()
        target_service = TargetService(gameplay)
        delt_days = target_service._delt_days(dead_line)
        if delt_days < 15 or delt_days > 365:
            ret[0] = ErrorCode.DATETIME_GAP_SHORT
            ret[1] = ErrorCode.error_message(ret[0])
            return json.dumps(ret)
        userinfo = dao_account.search_account(lc_account)
        logger.info(userinfo.as_dict())
        if not userinfo:
            ret[0] = ErrorCode.ACCOUNT_NOT_EXIST
            ret[1] = ErrorCode.error_message(ret[0])
            return json.dumps(ret)
        userinfo = dao_daily.search_user_recent_info(lc_account)
        
        target_type = TargetType.from_str_to_type(target_type)
        if target_type != TargetType.Challenge and target_type != TargetType.ContinueDays:
            if not target_val or not target_val.isdigit():
                ret[0] = ErrorCode.VALUE_NOT_INT
                ret[1] = ErrorCode.error_message(ret[0])
                return json.dumps(ret)
            target_val = int(target_val)
        user_targets = target_service.get_user_unfinished_targets(
            lc_account)
        if user_targets:
            for item in user_targets:
                if item.target_type == target_type:
                    ret[0] = ErrorCode.TARGET_EXIST
                    ret[1] = ErrorCode.error_message(ret[0])
                    return json.dumps(ret)
        # info = [lc_account, target_type, 0, '', 1, td, dead_line, 0]
        info = TargetRecord()
        info.user = lc_account
        info.target_type = target_type
        info.create_date = td
        info.dead_line = dead_line

        if target_type == TargetType.Challenge:
            if not target_val or target_val == '':
                ret[0] = ErrorCode.OPPNENT_NOT_EXIST
                ret[1] = ErrorCode.error_message(ret[0])
                return json.dumps(ret)
            info.opponent = str(target_val)
        elif target_type == TargetType.ContinueDays:
            info.target_value = delt_days + userinfo.continue_days
            target_val = delt_days
        else:
            info.target_value = int(target_val)
        errcode, level = target_service.evaluate_target_level(
            lc_account, target_type, target_val=target_val, opponent=target_val, dead_line=dead_line)
        if errcode != 0:
            ret[0] = errcode
            ret[1] = ErrorCode.error_message(ret[0])
            return json.dumps(ret)
        info.level = level
        logger.info(info.as_dict())
        target_service.add_user_target(info)
        return json.dumps(ret)
    except Exception as ex:
        logger.warning(ex)
        ret[0] = ErrorCode.SERVER_ERROR
        ret[1] = ErrorCode.error_message(ret[0])
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
        dao_target = DaoTargetInfo()
        response = dao_target.get_user_target_info(pn, rn)
        
        data = []
        for info in response:
            item = info.as_dict()
            item['target_type'] = TargetType.from_type_to_str(
                int(item['target_type']))
            item['status'] = TargetStatus.from_status_to_str(
                int(item['status']))
            item['level'] = TargetLevel.from_level_to_str(int(item['level']))
            data.append(item)
        return json.dumps(data)
    except Exception as e:
        logger.warning(e)
        return json.dumps(ret)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=810)
    #app.run(host='127.0.0.1', port=810)

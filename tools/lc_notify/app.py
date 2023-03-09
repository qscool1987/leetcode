from flask import Flask
from flask import request
import datetime
import json
import sys
sys.path.append('./service')

import settings
from service.account_service import AccountService
from service.feedback_service import FeedbackService
from service.target_service import TargetInfoService
from service.daily_info_service import DailyInfoService
from service.interview_service import InterviewService
from loghandle import logger
from lc_error import ErrorCode

app = Flask(__name__)


@app.route('/all_user_daily_info')
def get_all_user_daily_info():
    ret = ['0', "succ"]
    try:
        daily_info_service = DailyInfoService()
        ret = daily_info_service.get_all_user_daily_info()
        return json.dumps(ret)
    except Exception as ex:
        logger.warning(ex)
        ret[0] = ErrorCode.MYSQL_SERVICE_ERR
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)


@app.route('/submit_account_info')
def submit_account_info():
    ret = ['0', "succ"]
    body = request.values
    logger.info(body)
    lc_account = body.get('lc_account')
    git_account = body.get('git_account')
    email = body.get('email_account')
    account_service = AccountService()
    try:
        ret = account_service.submit_account_info(lc_account, git_account, email)
        return json.dumps(ret)
    except Exception as ex:
        logger.warning(ex)
        ret[0] = ErrorCode.MYSQL_SERVICE_ERR
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)
    


@app.route('/submit_feedback_info')
def submit_feedback_info():
    ret = ['0', "succ"]
    body = request.values
    logger.info(body)
    content = body.get('msg')
    feedback_service = FeedbackService()
    try:
        ret = feedback_service.submit_feedback_info(content)
        return json.dumps(ret)
    except Exception as ex:
        logger.warning(ex)
        ret[0] = ErrorCode.SERVER_ERROR
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)


@app.route('/get_feedback_info')
def get_feedback_info():
    ret = ['0', "succ"]
    body = request.values
    logger.info(body)
    pn = body.get('pn')
    rn = body.get('rn')
    feedback_service = FeedbackService()
    try:
        ret = feedback_service.get_feedback_info(pn, rn)
        return json.dumps(ret)
    except Exception as ex:
        logger.warning(ex)
        ret[0] = ErrorCode.SERVER_ERROR
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)

@app.route('/get_interview_problem_info')
def get_interview_problem_info():
    ret = ['0', "succ"]
    body = request.values
    logger.info(body)
    pn = body.get('pn')
    rn = body.get('rn')
    pt = body.get('pt')
    interview_service = InterviewService()
    try:
        ret = interview_service.get_interview_problem_info(pn, rn, pt)
        return json.dumps(ret)
    except Exception as ex:
        logger.warning(ex)
        ret[0] = ErrorCode.SERVER_ERROR
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)

@app.route('/get_interview_problem_types')
def get_interview_problem_types():
    ret = ['0', "succ"]
    interview_service = InterviewService()
    try:
        ret = interview_service.get_interview_problem_types()
        return json.dumps(ret)
    except Exception as ex:
        logger.warning(ex)
        ret[0] = ErrorCode.SERVER_ERROR
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)

@app.route('/submit_target_info')
def submit_target_info():
    ret = ['0', "succ"]
    body = request.values
    logger.info(body)
    lc_account = body.get('lc_account')
    target_type = body.get('target_type')
    target_val = body.get('target_val')
    dead_line = body.get('dead_line')
    target_service = TargetInfoService()
    try:
        ret = target_service.submit_target_info(lc_account, target_type, target_val, dead_line)
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
    pn = body.get('pn')
    rn = body.get('rn')
    target_service = TargetInfoService()
    try:
        ret = target_service.get_target_info(pn, rn)
        return json.dumps(ret)
    except Exception as e:
        logger.warning(ex)
        ret[0] = ErrorCode.SERVER_ERROR
        ret[1] = ErrorCode.error_message(ret[0])
        return json.dumps(ret)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=810)
    #app.run(host='127.0.0.1', port=810)

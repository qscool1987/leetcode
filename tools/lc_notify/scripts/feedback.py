import os
import sys
import datetime
sys.path.append('..')
sys.path.append('../dao')
from dao.daily_info_dao import DaoDailyInfo
from dao.account_info_dao import DaoAccountInfo
from dao.feedback_dao import DaoFeedback

dao_feedback = DaoFeedback()

def update_feedback_answer(id, answer):
    dao_feedback.update_feedback_answer(id, answer)


def update_feedback_status(id, status):
    dao_feedback.update_feedback_status(id, status)
    

def add_feedback(content):
    td = datetime.date.today()
    dao_feedback.add_feedback_info(td, content)

id = 36
s = "目标为竞赛分数则可以提前完成，目标为挑战pk则只有等到结束日期才会比较结果"
content = "感谢 @ericyu 报的bug，账号绑定后显示成功，但账户未再主页显示"
add_feedback(content)

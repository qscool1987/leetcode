import os
import sys
import datetime
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


def update_feedback_answer(id, answer):
    import mysql_service
    sql_service = mysql_service.MysqlService()
    sql_service.update_feedback_answer(id, answer)


def update_feedback_status(id, status):
    import mysql_service
    sql_service = mysql_service.MysqlService()
    sql_service.update_feedback_status(id, status)
    

def add_feedback(content):
    import mysql_service
    td = datetime.date.today()
    sql_service = mysql_service.MysqlService()
    sql_service.add_feedback_info(td, content)

id = 36
s = "目标为竞赛分数则可以提前完成，目标为挑战pk则只有等到结束日期才会比较结果"
content = "感谢 @ericyu 报的bug，账号绑定后显示成功，但账户未再主页显示"
add_feedback(content)

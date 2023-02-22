import os
import sys
import datetime
import random
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


def open_user_lc_game(user, status):
    import mysql_service
    import lc_service
    leetcode_service = lc_service.LeetcodeService()
    sql_service = mysql_service.MysqlService()
    # 重新设置用户账户的基本信息，coins，medal，status
    acc_info = sql_service.search_account(user)
    his_coins = acc_info[6]
    his_medal = acc_info[2]

    medal = leetcode_service.get_user_medal_info(user)
    # coins = 100
    if medal == 1 and (mdeal & his_medal) == 0:
        his_coins += 30
    if medal == 2 and ((mdeal & his_medal) == 0):
        medal = 3
        his_medal += 50
    sql_service.update_user_coins(user, his_coins)
    sql_service.update_user_medal(user, medal)
    sql_service.update_account_status(user, status)
    # 更新用户每日统计信息
    td = str(datetime.date.today())
    user_daily_info = sql_service.serach_single_user_daily_info(
        user, td)  # 查看今天用户是否存在
    score = leetcode_service.get_user_score_info(user)
    info = leetcode_service.get_user_lc_stat_info(user)
    info[4] = score
    info[5] = 1
    info[6] = 0
    if not user_daily_info:
        sql_service.add_single_user_daily_info(td, info)
    else:
        sql_service.update_single_user_daily_info(td, info)


def update_user_total_days():
    import mysql_service
    sql_service = mysql_service.MysqlService()
    user_to_git, user_medal, user_award, user_email = sql_service.load_all_account_infos()
    for user in user_medal:
        days = sql_service.count_user_total_days(user)
        cnt = days[0][0]
        sql_service.update_user_total_days(user, cnt)


def random_char():
    chars = "abcdefghigklmnopqrstuvwxyz"
    k = random.randint(0, 25)
    return chars[k]


def generate_user_token():
    import mysql_service
    sql_service = mysql_service.MysqlService()
    user_to_git, user_medal, user_award, user_email = sql_service.load_all_account_infos()

    for user in user_medal:
        token = ''
        for i in range(0, 8):
            token += random_char()
        sql_service.update_user_token(user, token)


update_user_total_days()

import os
import sys
import datetime
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

def open_user_lc_game(user, status):
    import mysql_service
    import lc_service
    leetcode_service = lc_service.LeetcodeService()
    sql_service = mysql_service.MysqlService()
    #重新设置用户账户的基本信息，coins，medal，status
    medal = leetcode_service.get_user_medal_info(user)
    coins = 100
    if medal == 1:
        coins += 30
    if medal == 2:
        medal = 3
        coins += 80
    sql_service.update_user_coins(user, coins)
    sql_service.update_user_medal(user, medal)
    sql_service.update_account_status(user, status)
    # 更新用户每日统计信息
    td = str(datetime.date.today())
    user_daily_info = sql_service.serach_single_user_daily_info(user, td) #查看今天用户是否存在
    score = leetcode_service.get_user_score_info(user)
    info = leetcode_service.get_user_lc_stat_info(user)
    info[4] = score
    info[5] = 1
    info[6] = 0
    if not user_daily_info:
        sql_service.add_single_user_daily_info(td, info)
    else:
        sql_service.update_single_user_daily_info(td, info)
    
user = 'ljk202009'
open_user_lc_game(user, 0)

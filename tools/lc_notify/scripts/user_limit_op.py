import os
import sys
import datetime
import random
sys.path.append('..')
sys.path.append('../dao')
from dao.daily_info_dao import DaoDailyInfo
from dao.account_info_dao import DaoAccountInfo
import lc_service


def open_user_lc_game(user, status):
    leetcode_service = lc_service.LeetcodeService()
    dao_daily = DaoDailyInfo()
    dao_account = DaoAccountInfo()
    # 重新设置用户账户的基本信息，coins，medal，status
    acc_info = dao_account.search_account(user)
    his_coins = acc_info.coins
    his_medal = acc_info.medal

    medal = leetcode_service.get_user_medal_info(user)
    # coins = 100
    if medal == 1 and (mdeal & his_medal) == 0:
        his_coins += 30
    if medal == 2 and ((mdeal & his_medal) == 0):
        medal = 3
        his_medal += 50
    dao_account.update_user_coins(user, his_coins)
    dao_account.update_user_medal(user, medal)
    dao_account.update_account_status(user, status)
    # 更新用户每日统计信息
    td = str(datetime.date.today())
    user_daily_info = dao_daily.serach_single_user_daily_info(
        user, td)  # 查看今天用户是否存在
    score = leetcode_service.get_user_score_info(user)
    info = leetcode_service.get_user_lc_stat_info(user)
    info.rating_score = score
    info.date_time = td
    # print(info.as_dict())
    if not user_daily_info:
        dao_daily.add_single_user_daily_info(info)
    else:
        dao_daily.update_single_user_daily_info(td, info)


def random_char():
    chars = "abcdefghigklmnopqrstuvwxyz"
    k = random.randint(0, 25)
    return chars[k]


def generate_user_token():
    dao_account = DaoAccountInfo()
    user_infos = dao_account.load_all_account_infos()
    for user, item in user_infos.items():
        token = ''
        for i in range(0, 8):
            token += random_char()
        dao_account.update_user_token(user, token)


# user = 'zhi-xing-8ec'
# open_user_lc_game(user, 0)

generate_user_token()


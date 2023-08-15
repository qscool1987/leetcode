import os
import sys
import datetime
import random
sys.path.append('..')
sys.path.append('../dao')
import lc_service
from dao.account_info_dao import DaoAccountInfo
from dao.daily_info_dao import DaoDailyInfo
from dao.dao import Dao
from email_service import EmailService


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
    if medal == 2 and ((medal & his_medal) == 0):
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
        dao_daily.update_single_user_daily_info(info)


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


def send_award(user):
    dao_acc = DaoAccountInfo()
    
    award_str = """恭喜您在网站积分排名中名列前矛，感谢对网站的认可和贡献，同时也表示鼓励 \
        有一份小礼物要送给您，辛苦填写一下快递地址，收件人信息和电话号码～ \
        回复此邮件即可!!\n 请放心，所有信息会严格保密。"""
    award_str = """恭喜您完成UNBELIEVABLE难度目标，实现自我突破。感谢对网站的认可和贡献，同时也表示鼓励 \
        有一份小礼物要送给您，辛苦填写一下快递地址，收件人信息和电话号码～ \
        回复此邮件即可!!\n 请放心，所有信息会严格保密。"""
    user_info = dao_acc.search_account(user)
    if user_info.email != '':
        print(user_info.email, award_str)
        EmailService.send_email(user_info.email, award_str)

user = 'train_sky'
open_user_lc_game(user, 0)

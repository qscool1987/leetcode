import os
import sys
import datetime
import json
sys.path.append('..')
sys.path.append('../dao')
from dao.daily_info_dao import DaoDailyInfo
from dao.account_info_dao import DaoAccountInfo


def recover_coins():
    dao_account = DaoAccountInfo()
    filename = "scores"
    fp = open(filename)
    coins = json.loads(fp.read())
    for u, td_coins in coins.items():
        his_coins = dao_account.search_user_coins(u)
        # print(u, td_coins)
        if td_coins > 0: #说明之前加了，现在要减少
            print(u, td_coins,his_coins, 'xxxx')
            # dao_account.update_user_coins(u, his_coins + td_coins)
        # else:
        #     dao_account.update_user_coins(u, his_coins - td_coins)
            
recover_coins()
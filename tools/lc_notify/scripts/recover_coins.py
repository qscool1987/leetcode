import os
import sys
import datetime
import json
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


def recover_coins():
    import mysql_service
    sql_service = mysql_service.MysqlService()
    filename = "scores"
    fp = open(filename)
    coins = json.loads(fp.read())
    for u, td_coins in coins.items():
        his_coins = sql_service.search_user_coins(u)
        if td_coins > 0:
            sql_service.update_user_coins(u, his_coins - td_coins)
        else:
            sql_service.update_user_coins(u, his_coins + td_coins)
            
recover_coins()
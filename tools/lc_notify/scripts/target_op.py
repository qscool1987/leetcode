import os
import sys
import datetime
import random
# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
sys.path.append('..')
sys.path.append('../dao')
from dao.daily_info_dao import DaoDailyInfo
from dao.account_info_dao import DaoAccountInfo
from dao.target_info_dao import DaoTargetInfo
import lc_service
from lc_target import TargetStatus, TargetLevel, TargetType, TargetService
import game_play

def deal_user_target():
    dao_target = DaoTargetInfo()
    dao_account = DaoAccountInfo()
    dao_daily = DaoDailyInfo()
    game = game_play.GamePlay()
    
    target_service = TargetService(game)
    td = '2023-02-28'
    target_service.deal_all_targets_status_before_day(td)
    
def set_target_fail_before_day(day):
    dao_target = DaoTargetInfo()
    resp = dao_target.get_all_targets_befor_day(day)
    for item in resp:
        print(item.dead_line, item.user, item.status)
        dao_target.update_user_target_status(item.id, TargetStatus.FAIL)
    
    
set_target_fail_before_day('2023-02-28')
    
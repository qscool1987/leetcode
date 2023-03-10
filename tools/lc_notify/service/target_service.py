import datetime
import sys
sys.path.append('..')
sys.path.append('../dao')
from dao.target_info_dao import TargetRecord, DaoTargetInfo
from dao.daily_info_dao import DaoDailyInfo
from dao.account_info_dao import DaoAccountInfo
from lc_error import ErrorCode
from game_play import GamePlay
from lc_target import (TargetType, TargetStatus, TargetService, TargetLevel)


class TargetInfoService(object):
    def __init__(self):
        self.dao_daily = DaoDailyInfo()
        self.gameplay = GamePlay()
        self.dao_account = DaoAccountInfo()
        self.target_service = TargetService(self.gameplay)
        self.dao_target = DaoTargetInfo()
        self._lower_limit = 15
        self._upper_limit = 360
    
    def submit_target_info(self, lc_account, target_type, target_val, dead_line):
        td = datetime.date.today()
        ret = ['0', "succ"]
        if not dead_line:
            ret[0] = ErrorCode.DATETIME_GAP_SHORT
            ret[1] = ErrorCode.error_message(ret[0])
            return ret
        delt_days = self.target_service._delt_days(dead_line)
        if delt_days < self._lower_limit or delt_days > self._upper_limit:
            ret[0] = ErrorCode.DATETIME_GAP_SHORT
            ret[1] = ErrorCode.error_message(ret[0])
            return ret
        userinfo = self.dao_account.search_account(lc_account)
        if not userinfo:
            ret[0] = ErrorCode.ACCOUNT_NOT_EXIST
            ret[1] = ErrorCode.error_message(ret[0])
            return ret
        userinfo = self.dao_daily.search_user_recent_info(lc_account)
        target_type = TargetType.from_str_to_type(target_type)
        if target_type != TargetType.Challenge and target_type != TargetType.ContinueDays:
            if not target_val or not target_val.isdigit():
                ret[0] = ErrorCode.VALUE_NOT_INT
                ret[1] = ErrorCode.error_message(ret[0])
                return ret
            target_val = int(target_val)
        user_targets = self.target_service.get_user_unfinished_targets(
            lc_account)
        if user_targets:
            for item in user_targets:
                if item.target_type == target_type:
                    ret[0] = ErrorCode.TARGET_EXIST
                    ret[1] = ErrorCode.error_message(ret[0])
                    return ret
        info = TargetRecord()
        info.user = lc_account
        info.target_type = target_type
        info.create_date = td
        info.dead_line = dead_line
        if target_type == TargetType.Challenge:
            if not target_val or target_val == '':
                ret[0] = ErrorCode.OPPNENT_NOT_EXIST
                ret[1] = ErrorCode.error_message(ret[0])
                return ret
            info.opponent = str(target_val)
        elif target_type == TargetType.ContinueDays:
            info.target_value = delt_days + userinfo.continue_days
            target_val = delt_days
        else:
            info.target_value = int(target_val)
        errcode, level = self.target_service.evaluate_target_level(
            lc_account, target_type, target_val=target_val, opponent=target_val, dead_line=dead_line)
        if errcode != 0:
            ret[0] = errcode
            ret[1] = ErrorCode.error_message(ret[0])
            return ret
        info.level = level
        self.target_service.add_user_target(info)
        return ret

    def get_target_info(self, pn, rn):
        pn = int(pn)
        if pn < 1:
            pn = 1
        rn = int(rn)
        pn = (pn - 1) * rn
        response = self.dao_target.get_user_target_info(pn, rn)
        data = []
        for info in response:
            item = info.as_dict()
            item['target_type'] = TargetType.from_type_to_str(
                int(item['target_type']))
            item['status'] = TargetStatus.from_status_to_str(
                int(item['status']))
            item['level'] = TargetLevel.from_level_to_str(int(item['level']))
            data.append(item)
        return data
    
    
if __name__ == '__main__':
    obj = TargetInfoService()
    res = obj.get_target_info(0, 100)
    print(res)
        
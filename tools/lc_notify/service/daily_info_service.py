from dao.account_info_dao import DaoAccountInfo, AccountInfoRecord
from dao.daily_info_dao import DaoDailyInfo, UserDailyInfoRecord
import settings
import datetime
import json
import sys
sys.path.append('..')
sys.path.append('../dao')


class DailyInfoService(object):
    def __init__(self):
        self.daoAccount = DaoAccountInfo()
        self.daoUserDailyInfo = DaoDailyInfo()

    def get_all_user_daily_info(self):
        td = datetime.date.today()
        yd = td + datetime.timedelta(days=-1)
        data = self.daoUserDailyInfo.load_all_user_daily_info_by_day(td)
        if not data:
            data = self.daoUserDailyInfo.load_all_user_daily_info_by_day(yd)
        user_coins = self.daoAccount.load_all_account_coins()
        info = []
        for u, item in data.items():
            obj = item.as_dict()
            if u in user_coins:
                obj['coins'] = user_coins[u]
                obj['honer_level'] = settings.HonerLevel.from_level_to_str(
                    user_coins[u])
            else:
                continue
            lazydays = obj['lazy_days']
            if lazydays >= settings.LazyLevel.LEVEL16:
                obj['lazy_days'] = settings.LazyLevel.from_level_to_str(
                    settings.LazyLevel.LEVEL16)
            else:
                obj['lazy_days'] = settings.LazyLevel.from_level_to_str(
                    lazydays)
            info.append(obj)
        # 按今日刷题量进行排序
        info = sorted(info, key=lambda item: int(item['coins']), reverse=True)
        return info


if __name__ == '__main__':
    obj = DailyInfoService()
    res = obj.get_all_user_daily_info()
    print(res)

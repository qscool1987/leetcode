# coding=utf-8
#!/usr/bin/env python
import json
import requests
import datetime
import settings
from loghandle import logger
from daily_info_dao import DaoDailyInfo, UserDailyInfoRecord
from account_info_dao import DaoAccountInfo, AccountInfoRecord
import lc_service
from concurrent.futures import as_completed, ThreadPoolExecutor
import game_play
import sys

user_list2 = ['smilecode-2']  # 用于调试

# 访问leetcode官方接口的对象
dao_daily_info = DaoDailyInfo()
leetcode_service = lc_service.LeetcodeService()


def task(user_list, yd_infos, td, hour):
    dao = DaoDailyInfo()
    td_infos = {}
    for u in user_list:
        t_l = leetcode_service.get_user_lc_stat_info(u)
        if not t_l:
            continue
        # 获取竞赛分数信息
        score = leetcode_service.get_user_score_info(u)
        t_l.rating_score = score
        y_l = None
        if u in yd_infos:
            y_l = yd_infos[u]
        if not y_l:
            t_l.new_solve = 0
        else:
            diff_t = int(t_l.total_solve) - int(y_l.total_solve)
            t_l.new_solve = 0
            if diff_t > 0:
                t_l.continue_days = y_l.continue_days + 1
                t_l.lazy_days = y_l.lazy_days - 2
                t_l.total_days = y_l.total_days + 1
                if t_l.lazy_days < 0:  # 最低不低于0
                    t_l.lazy_days = 0
                # hard, mid,easy分别刷的题量
                t_l.hard_num = t_l.hard_total - y_l.hard_total
                t_l.mid_num = t_l.mid_total - y_l.mid_total
                t_l.easy_num = t_l.easy_total - y_l.easy_total
                t_l.new_solve = t_l.hard_num * 3 + t_l.mid_num * 2 + t_l.easy_num
            else:
                # 如果今天晚上23点后统计还是没有刷题，则懒懒等级+1
                if hour >= 23:
                    t_l.continue_days = 0
                    t_l.lazy_days = y_l.lazy_days + 1
                    t_l.total_days = y_l.total_days
                    t_l.hard_num = 0
                    t_l.mid_num = 0
                    t_l.easy_num = 0
                else:
                    t_l.continue_days = y_l.continue_days
                    t_l.lazy_days = y_l.lazy_days
                    t_l.total_days = y_l.total_days
                    t_l.hard_num = 0
                    t_l.mid_num = 0
                    t_l.easy_num = 0
                if t_l.lazy_days > settings.LazyLevel.LEVEL16:
                    t_l.lazy_days = settings.LazyLevel.LEVEL16
        # 将最新的用户统计信息写入数据看
        info = dao.serach_single_user_daily_info(user, td)
        item.date_time = td
        if not info:
            dao.add_single_user_daily_info(item)
        else:
            dao.update_single_user_daily_info(item)
        td_infos[u] = t_l
    return td_infos


def stat_user_info():
    """
    统计所有用户的刷题信息并进行汇总，和昨日信息进行对比，将结果记录到mysql
    """
    td = datetime.date.today()
    yd = td + datetime.timedelta(days=-1)
    td_infos = {}
    td = str(td)
    yd = str(yd)
    dao_account = DaoAccountInfo()
    # 从数据库加载昨天的统计信息, 账户映射信息, 奖牌信息
    yd_infos = dao_daily_info.load_all_user_daily_info_by_day(yd)
    account_infos = dao_account.load_all_account_infos()
    user_list = []
    for u, item in account_infos.items():
        if item.status == 0:
            user_list.append(u)
    hour = datetime.datetime.now().hour
    pool = ThreadPoolExecutor(max_workers=6)
    k = 0
    LIMIT = 20
    futures = []
    while k < len(user_list):
        # 获取刷题信息
        future = pool.submit(task, user_list[k: k + LIMIT], yd_infos, td, hour)
        futures.append(future)
        k += LIMIT
    for future in as_completed(futures):
        if future.exception():
            continue
        data = future.result()
        td_infos.update(data)
    # result = []
    # for u, v in td_infos.items():
    #     result.append(v.as_dict())
    # print(len(result), json.dumps(result))
    logger.info("add into mysql finished")
    # 游戏逻辑
    gameplay = game_play.GamePlay(td_infos, yd_infos)
    if hour == 6:
        gameplay.publish_rand_problem(td)
    if hour >= 23:
        logger.info("begin to play game!")
        gameplay.run(td)
        logger.info("end play game!")


if __name__ == '__main__':
    import time
    t1 = time.time()
    stat_user_info()
    t2 = time.time()
    logger.info("本次执行更新耗时: {}".format(t2 - t1))

import os
import sys
import datetime
sys.path.append('..')
sys.path.append('../dao')
from daily_info_dao import DaoDailyInfo
from account_info_dao import DaoAccountInfo
from target_info_dao import DaoTargetInfo
import  pandas  as pd
from pandas import DataFrame
from lc_target import (TargetType, TargetLevel, TargetStatus)
import json

# import matplotlib.pyplot as plt

# def show_rating():
#     plt.rcParams['font.sans-serif'] = ['SimHei']  # 添加这条可以让图形显示中文
#     x_axis_data = [1, 2, 3, 4, 5]
#     y_axis_data = [1, 2, 3, 4, 5]
#     # plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，透明度,线的宽度和标签
#     plt.plot(x_axis_data, y_axis_data, 'ro-', color='#4169E1', alpha=0.8, linewidth=1, label='一些数字')
#     # 显示标签，如果不加这句，即使在plot中加了label='一些数字'的参数，最终还是不会显示标签
#     plt.legend(loc="upper right")
#     plt.xlabel('x轴数字')
#     plt.ylabel('y轴数字')
#     plt.show()


def write_to_excel(data_list):
    title = {
        "user": '用户',
        "days": '进群天数',
        "acc_days": '累积打卡天数',
        "pdt": '总刷题增量',
        "sdt": '竞赛分数增量',
        "jdt": '刷题积分',
        "cql": '出勤率',
        "avgp": '日均刷题量',
        "s_problem":  '初始刷题量',
        "e_problem":  '当前刷题量',
        "s_score": '起始竞赛分',
        "e_score": '当前竞赛分',
    }
    pdfs = []
    for data in data_list:
        content = {}
        for key, val in data.items():
            content[title[key]] = val
        pdf = pd.DataFrame(content)
        pdfs.append(pdf)
    with pd.ExcelWriter('1.xlsx', mode='w') as writer:
        for i, pdf in enumerate(pdfs):
            sheet_name = "Sheet" + str(i+1)
            pdf.to_excel(writer, sheet_name=sheet_name, index=False)
            
def generate_excel_table(data_list):
    title = {
        "user": '用户',
        "coins": '积分',
        "coins_rank": '积分排名',
        "days": '进群天数',
        "acc_days": '累积打卡天数',
        "acc_days_rank": '累积打卡天数排名',
        "cql": '出勤率',
        "cql_rank": '出勤率排名',
        "s_problem": '初始刷题量',
        "s_problem_rank": '初始刷题量排名',
        "e_problem": '当前刷题量',
        "e_problem_rank": '当前刷题量排名',
        "dt_problem": '刷题增量',
        "dt_problem_rank": '刷题增量排名',
        "avgp": '日均刷题量',
        "avgp_rank": '日均刷题量排名',
        "s_score": '竞赛初始分数',
        "s_score_rank": '竞赛初始分数排名',
        "e_score": '竞赛当前分数',
        "e_score_rank": '竞赛当前分数排名',
        "dt_score": '竞赛增量分数',
        "dt_score_rank": '竞赛增量分数排名',
        "target_score": '目标完成得分',
        "target_score_rank": '目标完成得分排名',
        "solve_max": '最勤奋的那一天完成的题量',
        "d_solve_max": '最勤奋那天的日期',
        "rating_max": '上分最多那天的得分',
        "d_rating_max": '上分最多的那天的日期'
    }
    pdfs = []
    for data in data_list:
        content = {}
        for key, val in data.items():
            content[title[key]] = val
        pdf = pd.DataFrame(content)
        pdfs.append(pdf)
    with pd.ExcelWriter('summary_table.xlsx', mode='w') as writer:
        for i, pdf in enumerate(pdfs):
            sheet_name = "Sheet" + str(i+1)
            pdf.to_excel(writer, sheet_name=sheet_name, index=False)
    
    

"""
0.累计打卡天数，入群总天数 出勤率 = 累积打卡天数 / 入群总天数    
2.刷题总量增量，日均刷题数量
3.竞赛积分增量 dt
4.积分增量
5.目标达人
6.2200以下最大进步奖
"""

def stat_user_info():
    dao_account = DaoAccountInfo()
    dao_daily = DaoDailyInfo()
    
    infos = dao_daily.load_all_user_daily_infos()
    accounts = dao_account.load_all_accounts()
    user_d_infos = {}
    for info in infos:
        u = info.user
        if u not in user_d_infos:
            user_d_infos[u] = []
        user_d_infos[u].append(info)
    for u in user_d_infos:
        infos = user_d_infos[u]
        user_d_infos[u] = sorted(infos, key=lambda data: data.date_time)

    # print(user_d_infos)
    ac_infos = []
    for u in user_d_infos:
        infos = user_d_infos[u]
        dt = infos[-1].date_time - infos[0].date_time
        dt = dt.days + 1
        if dt <= 0:
            continue
        # print(dt)
        acc = infos[-1].total_days
        pdt = infos[-1].total_solve - infos[0].total_solve
        sdt = infos[-1].rating_score - infos[0].rating_score
        account = accounts.get(u)
        if not account:
            continue
        jdt = account.coins
        
        item = {
            "user": u,
            "days": dt, # 进群天数
            "acc_days": acc, # 累积打卡天数
            "pdt": pdt, # 总刷题增量
            "sdt": sdt, # rating_score 增量
            "jdt": jdt, # coins 增量
            "cql": float("%.2f" % (acc / dt)), # 出勤率
            "avgp": float("%.2f" %  (pdt / dt)), # 日均刷题量
            "s_problem":  infos[0].total_solve, # 进群时刷题量
            "e_problem":  infos[-1].total_solve, # 当前刷题量
            "s_score": infos[0].rating_score, # 进群时rating_score
            "e_score": infos[-1].rating_score, # 当前rating_score
        }
        ac_infos.append(item)
    # 1. 累积打卡天数
    ac_infos = sorted(ac_infos, key=lambda item: item['acc_days'], reverse=True)
    resp = []
    data_list = {
        'user' : [],
        'acc_days': [],
        'days': [],
        'cql': []
    }
    for info in ac_infos[:10]:
        data_list['user'].append(info['user'])
        data_list['acc_days'].append(info['acc_days'])
        data_list['days'].append(info['days'])
        data_list['cql'].append(info['cql'])
    resp.append(data_list)
    #2.刷题总量增量，日均刷题数量
    
    data_list2 = {
        'user': [],
        'pdt': [],
        'days': [],
        'avgp': []
    }
    ac_infos = sorted(ac_infos, key=lambda item: item['avgp'], reverse=True)
    for info in ac_infos[:10]:
        data_list2['user'].append(info['user'])
        data_list2['pdt'].append(info['pdt'])
        data_list2['days'].append(info['days'])
        data_list2['avgp'].append(info['avgp'])
        
    data_list3 = {
        'user': [],
        'pdt' : [],
        'days': [],
        's_problem': [],
        'e_problem': []
    }
    ac_infos = sorted(ac_infos, key=lambda item: item['pdt'], reverse=True)
    for info in ac_infos[:10]:
        data_list3['user'].append(info['user'])
        data_list3['pdt'].append(info['pdt'])
        data_list3['days'].append(info['days'])
        data_list3['s_problem'].append(info['s_problem'])
        data_list3['e_problem'].append(info['e_problem'])

    rating = []
    data_list4 = {
        'user':[],
        'sdt': [],
        'days':[],
        's_score': [],
        'e_score': []
    }
    ac_infos = sorted(ac_infos, key=lambda item: item['sdt'], reverse=True)
    for info in ac_infos[:20]:
        item = {
            "user": info['user'],
            "sdt": info['sdt'],
            "days": info['days'],
            "s_score": info['s_score'],
            "e_score": info['e_score'],
        }
        if item['s_score'] > 0:
            rating.append(item)
            if len(rating) > 10:
                break
            data_list4['user'].append(info['user'])
            data_list4['sdt'].append(info['sdt'])
            data_list4['days'].append(info['days'])
            data_list4['s_score'].append(info['s_score'])
            data_list4['e_score'].append(info['e_score'])

    ac_infos = sorted(ac_infos, key=lambda item: item['jdt'], reverse=True)
    data_list5 = {
        'user': [],
        'jdt': [],
        'days': [],
        'acc_days': [],
        'cql': [],
        'pdt': [],
        'avgp': [],
        'sdt': [],
        's_score': [],
        'e_score': []
    }
    for info in ac_infos:
        data_list5['user'].append(info['user'])
        data_list5['jdt'].append(info['jdt'])
        data_list5['days'].append(info['days'])
        data_list5['acc_days'].append(info['acc_days'])
        data_list5['cql'].append(info['cql'])
        data_list5['pdt'].append(info['pdt'])
        data_list5['avgp'].append(info['avgp'])
        data_list5['sdt'].append(info['sdt'])
        data_list5['s_score'].append(info['s_score'])
        data_list5['e_score'].append(info['e_score'])
    resp.append(data_list2)
    resp.append(data_list3)
    resp.append(data_list4)
    resp.append(data_list5)
    write_to_excel(resp)
    
def get_user_target_score(user, target_infos):
    if user not in target_infos:
        return 0
    user_targets = target_infos[user]
    score = 0
    for target in user_targets:
        status = target.status
        level = target.level
        if status == TargetStatus.SUCC:
            score += TargetLevel.from_level_to_score(level)
        elif status == TargetStatus.FAIL:
            score -= TargetLevel.from_level_to_score(level) // 2
    return score

def binary_search(nums, target):
    i = 0
    j = len(nums)-1
    index = -1
    while i <= j:
        index = (i + j) // 2
        if nums[index] > target:
            i = index + 1
        elif nums[index] < target:
            j = index - 1
        else:
            break
    while index >= 0 and nums[index] <= target:
        index -= 1
    return index + 1

def get_user_max_daily_info(infos):
    solve_max = 0
    d_solve_max = infos[0].date_time
    rating_max = 0
    d_rating_max = infos[0].date_time
    for i in range(1, len(infos)):
        if infos[i].total_solve - infos[i-1].total_solve > solve_max:
            solve_max = infos[i].total_solve - infos[i-1].total_solve
            d_solve_max = infos[i].date_time
        pre_score = 1500
        current_score = 1500
        if infos[i].rating_score != 0:
            current_score = infos[i].rating_score
        if infos[i-1].rating_score != 0:
            pre_score = infos[i-1].rating_score
        if current_score - pre_score > rating_max:
            rating_max = current_score - pre_score
            d_rating_max = infos[i].date_time
    return solve_max, d_solve_max, rating_max, d_rating_max
    

def generate_user_data_table():
    dao_account = DaoAccountInfo()
    dao_daily = DaoDailyInfo()
    dao_target = DaoTargetInfo()
    
    infos = dao_daily.load_all_user_daily_infos()
    account_infos = dao_account.load_all_accounts()
    targets = dao_target.get_user_target_info(0, 10000)
    
    # 积分
    coins_list = []
    problem_s_num_list = []
    problem_e_num_list = []
    problem_dt_num_list = []
    problem_d_avg_list = []
    rating_s_num_list = []
    rating_e_num_list = []
    rating_dt_num_list = []
    acc_days_list = []
    cql_list = []
    target_score_list = []
    
    user_d_infos = {}
    for info in infos:
        u = info.user
        if u not in user_d_infos:
            user_d_infos[u] = []
        user_d_infos[u].append(info)
    for u in user_d_infos:
        infos = user_d_infos[u]
        user_d_infos[u] = sorted(infos, key=lambda data: data.date_time)
    target_infos = {}
    for target in targets:
        if target.user not in target_infos:
            target_infos[target.user] = []
        target_infos[target.user].append(target)
    
    ac_infos = []
    today = datetime.date.today()
    for u in user_d_infos:
        infos = user_d_infos[u]
        y = infos[0].date_time.year
        m = infos[0].date_time.month
        d = infos[0].date_time.day
        dt = today - datetime.date(y,m,d)
        dt = dt.days + 1
        if dt <= 0:
            continue
        acc = infos[-1].total_days
        pdt = infos[-1].total_solve - infos[0].total_solve
        account = account_infos.get(u)
        if not account:
            continue
        jdt = account.coins
        rating_s_num = 1500
        if infos[0].rating_score != 0:
            rating_s_num = infos[0].rating_score
        rating_e_num = 1500
        if infos[-1].rating_score != 0:
            rating_e_num = infos[-1].rating_score
        target_score = get_user_target_score(u, target_infos)
        item = {
            "user": u,
            "days": dt, # 进群天数
            "acc_days": acc, # 累积打卡天数
            "dt_problem": pdt, # 总刷题增量
            "coins": jdt, # coins 增量
            "cql": float("%.2f" % (acc / dt)), # 出勤率
            "avgp": float("%.2f" %  (pdt / dt)), # 日均刷题量
            "s_problem":  infos[0].total_solve, # 进群时刷题量
            "e_problem":  infos[-1].total_solve, # 当前刷题量
            "s_score": rating_s_num, # 进群时rating_score
            "e_score": rating_e_num, # 当前rating_score
            "dt_score": rating_e_num - rating_s_num,
            "target_score": target_score,
        }
        ac_infos.append(item)
        coins_list.append(item['coins'])
        problem_s_num_list.append(item['s_problem'])
        problem_e_num_list.append(item['e_problem'])
        problem_dt_num_list.append(item['dt_problem'])
        problem_d_avg_list.append(item['avgp'])
        rating_s_num_list.append(item['s_score'])
        rating_e_num_list.append(item['e_score'])
        rating_dt_num_list.append(item['dt_score'])
        acc_days_list.append(item['acc_days'])
        cql_list.append(item['cql'])
        target_score_list.append(item['target_score'])
    coins_list = sorted(coins_list, reverse=True)
    problem_s_num_list = sorted(problem_s_num_list, reverse=True)
    problem_e_num_list = sorted(problem_e_num_list, reverse=True)
    problem_dt_num_list = sorted(problem_dt_num_list, reverse=True)
    problem_d_avg_list = sorted(problem_d_avg_list, reverse=True)
    rating_s_num_list = sorted(rating_s_num_list, reverse=True)
    rating_e_num_list = sorted(rating_e_num_list, reverse=True)
    rating_dt_num_list = sorted(rating_dt_num_list, reverse=True)
    acc_days_list = sorted(acc_days_list, reverse=True)
    cql_list = sorted(cql_list, reverse=True)
    target_score_list = sorted(target_score_list, reverse=True)
    for info in ac_infos:
        index = binary_search(coins_list, info['coins'])
        info['coins_rank'] = index + 1
        index = binary_search(problem_s_num_list, info['s_problem'])
        info['s_problem_rank'] = index + 1
        index = binary_search(problem_e_num_list, info['e_problem'])
        info['e_problem_rank'] = index + 1
        index = binary_search(problem_dt_num_list, info['dt_problem'])
        info['dt_problem_rank'] = index + 1
        index = binary_search(problem_d_avg_list, info['avgp'])
        info['avgp_rank'] = index + 1
        index = binary_search(rating_s_num_list, info['s_score'])
        info['s_score_rank'] = index + 1
        index = binary_search(rating_e_num_list, info['e_score'])
        info['e_score_rank'] = index + 1
        index = binary_search(rating_dt_num_list, info['dt_score'])
        info['dt_score_rank'] = index + 1
        index = binary_search(acc_days_list, info['acc_days'])
        info['acc_days_rank'] = index + 1
        index = binary_search(cql_list, info['cql'])
        info['cql_rank'] = index + 1
        index = binary_search(target_score_list, info['target_score'])
        info['target_score_rank'] = index + 1
        user_daily_infos = user_d_infos[info['user']]
        solve_max, d_solve_max, rating_max, d_rating_max = get_user_max_daily_info(user_daily_infos)
        info['solve_max'] = solve_max
        info['d_solve_max'] = str(d_solve_max)[: 10]
        info['rating_max'] = rating_max
        info['d_rating_max'] = str(d_rating_max)[: 10]
    data_list = {
        "user": [],
        "coins": [],
        "coins_rank": [],
        "days": [],
        "acc_days": [],
        "acc_days_rank": [],
        "cql": [],
        "cql_rank": [],
        "s_problem": [],
        "s_problem_rank": [],
        "e_problem": [],
        "e_problem_rank": [],
        "dt_problem": [],
        "dt_problem_rank": [],
        "avgp": [],
        "avgp_rank": [],
        "s_score": [],
        "s_score_rank": [],
        "e_score": [],
        "e_score_rank": [],
        "dt_score": [],
        "dt_score_rank": [],
        "target_score": [],
        "target_score_rank": [],
        "solve_max": [],
        "d_solve_max": [],
        "rating_max": [],
        "d_rating_max": [],
    }
    for info in ac_infos:
        data_list['user'].append(info['user'])
        data_list['coins'].append(info['coins'])
        data_list['coins_rank'].append(info['coins_rank'])
        data_list['days'].append(info['days'])
        data_list['acc_days'].append(info['acc_days'])
        data_list['acc_days_rank'].append(info['acc_days_rank'])
        data_list['cql'].append(info['cql'])
        data_list['cql_rank'].append(info['cql_rank'])
        data_list['s_problem'].append(info['s_problem'])
        data_list['s_problem_rank'].append(info['s_problem_rank'])
        data_list['e_problem'].append(info['e_problem'])
        data_list['e_problem_rank'].append(info['e_problem_rank'])
        data_list['dt_problem'].append(info['dt_problem'])
        data_list['dt_problem_rank'].append(info['dt_problem_rank'])
        data_list['avgp'].append(info['avgp'])
        data_list['avgp_rank'].append(info['avgp_rank'])
        data_list['s_score'].append(info['s_score'])
        data_list['s_score_rank'].append(info['s_score_rank'])
        data_list['e_score'].append(info['e_score'])
        data_list['e_score_rank'].append(info['e_score_rank'])
        data_list['dt_score'].append(info['dt_score'])
        data_list['dt_score_rank'].append(info['dt_score_rank'])
        data_list['target_score'].append(info['target_score'])
        data_list['target_score_rank'].append(info['target_score_rank'])
        data_list['solve_max'].append(info['solve_max'])
        data_list['d_solve_max'].append(info['d_solve_max'])
        data_list['rating_max'].append(info['rating_max'])
        data_list['d_rating_max'].append(info['d_rating_max'])
    generate_excel_table([data_list])
    
    

"""
个人信息汇总
0.积分
    积分总量&排名
1.刷题总量
    初始量&排名，总量&排名，增量&排名，每日均值&排名，最勤奋那天，折线图
2.rating分数
    初始量&排名，总量&排名，增量&排名，上分最大的那周，折线图
3.打卡
    进群日期，进群天数，累计打卡天数&排名，出勤率&排名
    是否被淘汰，哪一天被淘汰
4.目标
    目标数量&排名
    每个目标信息和完成度，总获得分数
"""

generate_user_data_table()
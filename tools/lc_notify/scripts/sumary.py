import os
import sys
import datetime
sys.path.append('..')
sys.path.append('../dao')
from daily_info_dao import DaoDailyInfo
from account_info_dao import DaoAccountInfo


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
            "days": dt,
            "acc_days": acc,
            "pdt": pdt,
            "sdt": sdt,
            "jdt": jdt,
            "cql": acc / dt,
            "avgp": pdt / dt,
            "s_problem":  infos[0].total_solve,
            "e_problem":  infos[-1].total_solve,
            "s_score": infos[0].rating_score,
            "e_score": infos[-1].rating_score,
        }
        ac_infos.append(item)
    # 1. 累积打卡天数
    acc_days = []
    ac_infos = sorted(ac_infos, key=lambda item: item['acc_days'], reverse=True)
    print("持之以恒 top10")
    print("用户\t进群总天数\t累积打卡天数\t出勤率")
    for info in ac_infos[:10]:
        item = {
            "user": info['user'],
            "acc_days": info['acc_days'],
            "days": info['days'],
            "cql": info['cql'],
        }
        acc_days.append(item)
        print(item['user'] + "\t" + str(item['days']) + "\t" + str(item['acc_days']) + "\t" + str(item['cql']))
    #2.刷题总量增量，日均刷题数量
    
    avgp = []
    ac_infos = sorted(ac_infos, key=lambda item: item['avgp'], reverse=True)
    print("日均刷题 top10")
    print("用户\t进群总天数\t总新增题量\t日均刷题量")
    for info in ac_infos[:10]:
        item = {
            "user": info['user'],
            "pdt": info['pdt'],
            "days": info['days'],
            "avgp": info['avgp']
        }
        avgp.append(item)
        print(item['user'] + "\t" + str(item['days']) + "\t" + str(item['pdt']) + "\t" + str(item['avgp']))
    pdt = []
    ac_infos = sorted(ac_infos, key=lambda item: item['pdt'], reverse=True)
    print("刷题增量 top10")
    print("用户\t进群总天数\t总新增题量\t起始值\t当前值")
    for info in ac_infos[:10]:
        item = {
            "user": info['user'],
            "pdt": info['pdt'],
            "days": info['days'],
            "s_problem": info['s_problem'],
            "e_problem": info['e_problem'],
        }
        pdt.append(item)
        print(item['user'] + "\t" + str(item['days']) + "\t" + str(item['pdt']) + "\t" + str(item['s_problem']) + "\t" + str(item['e_problem']))
    rating = []
    ac_infos = sorted(ac_infos, key=lambda item: item['sdt'], reverse=True)
    print("竞赛分数增量 top10")
    print("用户\t进群总天数\t竞赛成绩增量\t初始值\t当前值")
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
            print(item['user'] + "\t" + str(item['days']) + "\t" + str(item['sdt']) + "\t" + str(item['s_score']) + "\t" + str(item['e_score']))
    jdt = []
    ac_infos = sorted(ac_infos, key=lambda item: item['jdt'], reverse=True)
    for info in ac_infos[:10]:
        item = {
            "user": info['user'],
            "jdt": info['jdt'],
            "days": info['days'],
        }
        jdt.append(item)

stat_user_info()
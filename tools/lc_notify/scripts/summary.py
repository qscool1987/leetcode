import os
import sys
import datetime
sys.path.append('..')
sys.path.append('../dao')
from daily_info_dao import DaoDailyInfo
from account_info_dao import DaoAccountInfo
import  pandas  as pd
from pandas import DataFrame



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
        
        
stat_user_info() 

    
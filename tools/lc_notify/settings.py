#coding=utf-8
import os

user_list = ['zerotrac2','smilecode-2', 'aween', 'zzz-4t8', 'ChinaYC', 'CNLYJ', 'linuxer',
            'slluosali', 'Vergissmeinncht', 'daydayup', 'flippedli-xiao-hua', 
            'caicodehh', 'cardioid-t', 'ou-hai-zijhu23dnz',
            'exciting-tesla7ck', 'lao-qi-e-r']
user_list2 = ['smilecode-2'] #用于调试

# no_email_users = [
#     'linuxer',
#     'cardioid-t', 
#     'exciting-tesla7ck'
#     ]

languages = ['C++', 'Java', 'Python3', 'MySQL', 'Ruby', 'Bash', 'Go']

emails = {
    'caicodehh': '1748493969@qq.com',
    'flippedli-xiao-hua': 'lizhenhua0202@163.com',
    'smilecode-2': '595949643@qq.com',
    'CNLYJ': '1910198192@qq.com',
    'zzz-4t8': '1192963064@qq.com',
    'aween': '376087731@qq.com',
    'lao-qi-e-r': '2460762414@qq.com',
    'slluosali': '1554548256@qq.com',
    'daydayup': 'jiangwr1996@163.com',
    'Vergissmeinncht': '1936800723@qq.com',
    'ChinaYC': 'liuyichaochina@gmail.com',
    'ou-hai-zijhu23dnz': '196082511@qq.com'
    }

git_users = ['qscool1987', 'Yunjia Liu', 'BigDataHua', 'CsustHh', 
        'yinghuacao282428','Ruinenstadt9029']

lc_to_git = {
        'smilecode-2': 'qscool1987', 
        'CNLYJ': 'Yunjia Liu',
        'flippedli-xiao-hua': 'BigDataHua',
        'Vergissmeinncht': 'Ruinenstadt9029',
        'caicodehh': 'CsustHh'
        }
excel_cols = ['用户', '题量', '代码行数', '题目贡献', '竞赛分数', '连续打卡', '今日刷题']

confFile = "global"
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = CURRENT_PATH
LOG_PATH = os.path.join(ROOT_PATH, 'log')
# GLOBAL_CONF_PATH = os.path.join(ROOT_PATH, 'conf')
DATA_PATH = os.path.join(ROOT_PATH, 'data')


if __name__ == '__main__':
    print(CURRENT_PATH, ROOT_PATH, LOG_PATH, DATA_PATH)

#coding=utf-8
import os

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

confFile = "global"
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = CURRENT_PATH
LOG_PATH = os.path.join(ROOT_PATH, 'log')
GLOBAL_CONF_PATH = os.path.join(ROOT_PATH, 'conf')
DATA_PATH = os.path.join(ROOT_PATH, 'data')


if __name__ == '__main__':
    print(CURRENT_PATH, ROOT_PATH, LOG_PATH, DATA_PATH)

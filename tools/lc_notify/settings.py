#coding=utf-8
import os

languages = ['C', 'C++', 'Java', 'Python3', 'MySQL', 'Ruby', 'Bash', 'Go']

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

class MedalType:
    """
    奖励类型
    """
    Knight = 1
    Guardian = 2
    CodeSubmit = 4
    ProblemSubmit = 8
    ContinueDays = 16


lazyLevels = ["正常", "懒惰萌芽期", "懒惰炼体期", "懒惰练气期", "懒惰筑基期",
        "懒惰结丹期", "懒惰元婴期", "懒惰化神期", "懒惰炼虚期", "懒惰合体期",
        "懒惰大乘期", "懒惰渡劫期", "懒惰真仙境", "懒惰金仙境", "懒惰太乙境",
        "懒惰大罗境", "懒惰道祖境"]


if __name__ == '__main__':
    print(CURRENT_PATH, ROOT_PATH, LOG_PATH, DATA_PATH)

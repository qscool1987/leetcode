# coding=utf-8
import os

confFile = "global"
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = CURRENT_PATH
LOG_PATH = os.path.join(ROOT_PATH, 'log')
GLOBAL_CONF_PATH = os.path.join(ROOT_PATH, 'conf')
DATA_PATH = os.path.join(ROOT_PATH, 'data')


lazyLevels = ["正常", "懒惰萌芽期", "懒惰炼体期", "懒惰练气期", "懒惰筑基期",
              "懒惰结丹期", "懒惰元婴期", "懒惰化神期", "懒惰炼虚期", "懒惰合体期",
              "懒惰大乘期", "懒惰渡劫期", "懒惰真仙境", "懒惰金仙境", "懒惰太乙境",
              "懒惰大罗境", "懒惰道祖境"]


if __name__ == '__main__':
    print(CURRENT_PATH, ROOT_PATH, LOG_PATH, DATA_PATH)

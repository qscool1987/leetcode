# coding=utf-8
import os

confFile = "global"
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = CURRENT_PATH
LOG_PATH = os.path.join(ROOT_PATH, 'log')
GLOBAL_CONF_PATH = os.path.join(ROOT_PATH, 'conf')
DATA_PATH = os.path.join(ROOT_PATH, 'data')


class LazyLevel:
    LEVEL0 = 0
    LEVEL1 = 1
    LEVEL2 = 2
    LEVEL3 = 3
    LEVEL4 = 4
    LEVEL5 = 5
    LEVEL6 = 6
    LEVEL7 = 7
    LEVEL8 = 8
    LEVEL9 = 9
    LEVEL10 = 10
    LEVEL11 = 11
    LEVEL12 = 12
    LEVEL13 = 13
    LEVEL14 = 14
    LEVEL15 = 15
    LEVEL16 = 16
    lazyLevels = ["正常", "懒惰萌芽期", "懒惰炼体期", "懒惰练气期", "懒惰筑基期",
                "懒惰结丹期", "懒惰元婴期", "懒惰化神期", "懒惰炼虚期", "懒惰合体期",
                "懒惰大乘期", "懒惰渡劫期", "懒惰真仙境", "懒惰金仙境", "懒惰太乙境",
                "懒惰大罗境", "懒惰道祖境"]

    @classmethod
    def from_level_to_str(cls, status):
        if status > LazyLevel.LEVEL16:
            return LazyLevel.lazyLevels[LazyLevel.LEVEL16]
        return LazyLevel.lazyLevels[status]


class FeedbackStatus:
    UNKNOW = 0
    PROCESSING = 1
    FINISHED = 2
    REJECTED = 3

    status_to_str = {
        0: "未知状态",
        1: "处理中",
        2: "处理完成",
        3: "不采纳"
    }

    @classmethod
    def from_status_to_str(cls, status):
        if status in FeedbackStatus.status_to_str:
            return FeedbackStatus.status_to_str[status]
        return "未知状态"


class RandomProblemStatus:
    UNKNOW = 0
    PROCESSING = 1
    FINISHED = 2
    FAILED = 3

    status_to_str = {
        0: "未知状态",
        1: "处理中",
        2: "处理完成",
        3: "失败"
    }

    @classmethod
    def from_status_to_str(cls, status):
        if status in RandomProblemStatus.status_to_str:
            return RandomProblemStatus.status_to_str[status]
        return "未知状态"


if __name__ == '__main__':
    print(CURRENT_PATH, ROOT_PATH, LOG_PATH, DATA_PATH)

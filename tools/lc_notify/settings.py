# coding=utf-8
import os
import math
confFile = "global"
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = CURRENT_PATH
LOG_PATH = os.path.join(ROOT_PATH, 'log')
GLOBAL_CONF_PATH = os.path.join(ROOT_PATH, 'conf')
DATA_PATH = os.path.join(ROOT_PATH, 'data')

class HonerLevel:
    honerLevels = {
        0 : "江湖白丁", #100
        1 : "武林新丁", #140
        2 : "江湖小虾", #180
        3 : "后起之秀", #220
        4 : "武林高手", #260
        5 : "风尘奇侠", #300
        6 : "无双隐士", #340
        7 : "世外高人", #400
        8 : "江湖侠隐", #480
        9 : "名满天下", #580
        10 : "陆地飞仙", #700
        11 : "无极天师", #840
        12 : "神机真人", #1000
        13 : "金身尊者", #1180
        14 : "天外飞仙", #1380
        15 : "无敌圣者", #1600
        16 : "三界贤君", #1840
        17 : "万圣天尊", #2100
        18 : "九天圣佛", #2380
        19 : "神通广大", #2680
        20 : "无所不能"  #3000
    }
    
    @classmethod
    def from_level_to_str(cls, score):
        if score <= 100:
            return HonerLevel.honerLevels[0]
        if score <= 340:
            level = math.ceil((score - 100) / 40)
            return HonerLevel.honerLevels[level]
        if score > 340 and score <= 400:
            level = 7
        elif score > 400 and score <= 480:
            level = 8
        elif score > 480 and score <= 580:
            level = 9
        elif score > 580 and score <= 700:
            level = 10
        elif score > 700 and score <= 840:
            level = 11
        elif score > 840 and score <= 1000:
            level = 12
        elif score > 1000 and score <= 1180:
            level = 13
        elif score > 1180 and score <= 1380:
            level = 14
        elif score > 1380 and score <= 1600:
            level = 15
        elif score > 1600 and score <= 1840:
            level = 16
        elif score > 1840 and score <= 2100:
            level = 17
        elif score > 2100 and score <= 2380:
            level = 18
        elif score > 2380 and score <= 2680:
            level = 19
        elif score > 2680:
            level = 20
        return HonerLevel.honerLevels[level]


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
    res = HonerLevel.from_level_to_str(861)
    print(res)

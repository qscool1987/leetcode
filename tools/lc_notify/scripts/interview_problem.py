import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


def add_interview_problem(infos):
    import mysql_service
    sql_service = mysql_service.MysqlService()
    for info in infos:
        content = info[0]
        answer = info[1]
        pt = info[2]
        company = info[3]
        jd = info[4]
        sql_service.add_interview_problem(content, answer, pt, company, jd)

infos = [
    ["判断一个字符串是否为一个有效的ipv4", '', "算法编程", "百度，蘑菇车联",''],
    ["给定一个字符串，将其转成double，说明：double不用考虑包含字符e的情况，不允许使用任何库函数", '', "算法编程", "快手", ''],
    ["给定一个字符串,只包含'o','O',两种字符，'oo'->'O', 'OO'->'', 从左向右处理，返回最终剩余字符串", '', "算法编程", "青藤云安全", ''],
    ["double开平方", '', "算法编程", "快手，阿里", ''],
    ["给定整数n打印n*n的蛇形矩阵", '', "算法编程", "百度，拼多多", ''],
    ["链表插入排序", '', "算法编程", "autox", ''],
    ["链表归并排序", '', "算法编程", "SmartNews，拼多多", ''],
    ["删除链表中的重复节点 [2,3,3,4,5,5,6,6] -> [2,4]", '', "算法编程", "autox", ''],
    ["给定一个n*n的整型矩阵，返回从(0,0)->(n-1,n-1)的一条代价最小的路径", '', "算法编程", "美团", ''],
    ["拓扑排序", '', "算法编程", "九坤", ''],
    ["3个线程，一个线程打印0，一个线程打印基数，一个线程打印偶数，交替输出: 0 1 2 0 3 4 0 5 6 0", '', "并发编程", "九坤，字节", ''],
    ["lru算法设计", '', "算法编程", "阿里，快手，滴滴", ''],
    ["英文输入法设计", '', "算法编程", "autox", ''],
    ["链表k个数据为一组进行反转 k=3   [1,2,3,4,5] -> [3,2,1,5,4]", '', "算法编程", "滴滴，小米", ''],
    ["给定一个先升后降的数组，查找指定元素k", '', "算法编程", "字节", ''],
    ["两个有序数组求交集 [1,2,3]和[2,3,4]->[2,3]", '', "算法编程", "快手", ''],
    ["给定一个字符串，找到其中的最长回文字串", '', "算法编程", "腾讯", ''],
    ["找出二叉树的最大路径和", '', "算法编程", "autox", ''],
    ["给定一个字符串，只包含'('和')',找出最长的有效括号匹配长度", '', "算法编程", "拼多多", ''],
    ["滑动窗口最大值", "", "算法编程", "美团", ''],
    ["一维接雨水", '', "算法编程", "毫末智行", '']
]

add_interview_problem(infos)
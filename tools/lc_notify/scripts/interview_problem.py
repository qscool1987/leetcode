from dao.interview_problem_dao import DaoInterviewProblem
import os
import sys
sys.path.append('..')
sys.path.append('../dao')

dao_interview = DaoInterviewProblem()


def add_interview_problem(infos):
    for info in infos:
        content = info[0]
        answer = info[1]
        pt = info[2]
        company = info[3]
        jd = info[4]
        dao_interview.add_interview_problem(content, answer, pt, company, jd)


infos = [
    ["判断一个字符串是否为一个有效的ipv4", '', "算法编程", "百度，蘑菇车联", ''],

]

add_interview_problem(infos)

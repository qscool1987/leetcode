"""sql object for each table"""
import sys
sys.path.append('..')
from dao.dao import Dao


class InterviewProblemRecord:
    def __init__(self):
        self.content = ''
        self.answer = 0
        self.type = 0
        self.company = 1
        self.jd = ''
        
    def as_dict(self):
        return {
            'content': self.content,
            'answer' : self.answer,
            'type': self.type,
            'company': self.company,
            'jd': self.jd,
        }


class DaoInterviewProblem(Dao):
    INTERVIEW_PROBLEM_INFO_TABLE = 'interview_problem_info'
    INTERVIEW_PROBLEM_INFO_FIELDS = [
        'content', 'answer', 'type', 'company', 'jd']
    problem_types = ["算法编程", "Java", "C++", "操作系统",
                 "计算机网络", "mysql", "redis", "mq", "并发编程", "分布式系统"]
    
    def load_interview_problems(self, pn, rn, pt=-1):
        if pt >= len(self.problem_types):
            return []
        if not self._connect_mysql():
            return False
        if pt == -1:
            sql = "select * from " + self.INTERVIEW_PROBLEM_INFO_TABLE + \
                " limit %s, %s" % (pn, rn)
        else:
            pt = self.problem_types[pt]
            sql = "select * from " + self.INTERVIEW_PROBLEM_INFO_TABLE + \
                " where type = '%s' limit %s, %s" % (pt, pn, rn)
        datas = self._query(sql)
        if not datas:
            return None
        resp = []
        for data in datas:
            item = InterviewProblemRecord()
            item.id = data[0]
            item.content = data[1]
            item.answer = data[2]
            item.type = data[3]
            item.company = data[4]
            item.jd = data[5]
            resp.append(item)
        return resp

    def add_interview_problem(self, item):
        if not self._connect_mysql():
            return False
        sql = "insert into " + self.INTERVIEW_PROBLEM_INFO_TABLE + " (" + \
            ",".join(self.INTERVIEW_PROBLEM_INFO_FIELDS) + ") values('%s', '%s', '%s', '%s', '%s')" \
            % (item.content, item.answer, item.type, item.company, item.jd)
        return self._add(sql)

    def update_interview_problem_answer(self, id, answer):
        sql = "update " + self.INTERVIEW_PROBLEM_INFO_TABLE + \
            " set answer = %s where id = %s" % (answer, id)
        return self._update(sql)

    def update_interview_problem_jd(self, id, jd):
        sql = "update " + self.INTERVIEW_PROBLEM_INFO_TABLE + \
            " set jd = %s where id = %s" % (jd, id)
        return self._update(sql)
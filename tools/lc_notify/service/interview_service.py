import sys
sys.path.append('..')
sys.path.append('../dao')
from dao.interview_problem_dao import DaoInterviewProblem


class InterviewService(object):
    def __init__(self):
        self.dao = DaoInterviewProblem()
    
    def get_interview_problem_types(self):
        result = DaoInterviewProblem.problem_types
        res = []
        for i in range(0, len(result)):
            res.append({"type": i, "name": result[i]})
        return res

    def get_interview_problem_info(self, pn, rn, pt=None):
        pn = int(pn)
        rn = int(rn)
        if not pt:
            pt = -1
        else:
            pt = int(pt)
        if pn < 1:
            pn = 1
        pn = (pn - 1) * rn
        datas = self.dao.load_interview_problems(pn, rn, pt)
        result = []
        for item in datas:
            result.append(item.as_dict())
        return result
    

if __name__ == '__main__':
    obj = InterviewService()
    res = obj.get_interview_problem_info(0, 100)
    print(res)
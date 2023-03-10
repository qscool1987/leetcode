import datetime
import sys
sys.path.append('..')
sys.path.append('../dao')
from dao.feedback_dao import DaoFeedback
from loghandle import logger
from lc_error import ErrorCode


class FeedbackService(object):
    def __init__(self):
        self.dao = DaoFeedback()
        pass
    
    def submit_feedback_info(self, content):
        ret = ['0', "succ"]
        date = datetime.date.today()
        if not self.dao.add_feedback_info(date, content):
            ret[0] = ErrorCode.SERVER_ERROR
            ret[1] = ErrorCode.error_message(ret[0])
        return ret
    
    def get_feedback_info(self, pn, rn):
        pn = int(pn)
        if pn < 1:
            pn = 1
        rn = int(rn)
        pn = (pn - 1) * rn
        logger.info("pn={}, rn={}".format(pn, rn))
        date = datetime.date.today()
        datas = self.dao.load_feedback_info(pn, rn)
        result = []
        for item in datas:
            result.append(item.as_dict())
        return result
    
    
if __name__ == '__main__':
    obj = FeedbackService()
    res = obj.get_feedback_info(0, 100)
    print(res)
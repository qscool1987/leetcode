"""sql object for each table"""
import sys
sys.path.append('..')
from dao.dao import Dao


class FeedbackRecord:
    def __init__(self):
        self.content = ''
        self.answer = ''
        self.date_time = ''
        self.status = 0
        self.id = 0
        
    def as_dict(self):
        return {
            'id': self.id,
            'content' : self.content,
            'answer': self.answer,
            'date_time': str(self.date_time),
            'status': self.status,
        }


class DaoFeedback(Dao):
    FEEDBACK_INFO_TABLE = 'feedback_info'
    FEEDBACK_INFO_FIELDS = ['content', 'status', 'answer', 'date_time']
    
    def __init__(self):
        pass
    
    def add_feedback_info(self, date, content):
        if not self._connect_mysql():
            return False
        sql = "insert into " + self.FEEDBACK_INFO_TABLE + " (" + \
            ",".join(self.FEEDBACK_INFO_FIELDS) + ") values('%s', %s, '%s', '%s')" \
            % (content, 1, '', date)
        return self._add(sql)

    def update_feedback_status(self, id, status):
        if not self._connect_mysql():
            return False
        sql = "update " + self.FEEDBACK_INFO_TABLE + \
            " set status = %s where id = %d" % (status, id)
        return self._update(sql)

    def update_feedback_answer(self, id, answer):
        if not self._connect_mysql():
            return False
        sql = "update " + self.FEEDBACK_INFO_TABLE + \
            " set answer = '%s' where id = %d" % (answer, id)
        return self._update(sql)

    def load_feedback_info(self, pn, rn):
        if not self._connect_mysql():
            return False
        sql = "select * from " + self.FEEDBACK_INFO_TABLE + \
            " order by date_time desc limit %s, %s" % (pn, rn)
        datas = self._query(sql)
        if not datas:
            return None
        resp = []
        for data in datas:
            item = FeedbackRecord()
            item.id = data[0]
            item.content = data[1]
            item.date_time = data[2]
            item.status = data[3]
            item.answer = data[4]
            resp.append(item)
        return resp
    
if __name__ == '__main__':
    obj = DaoFeedback()
    res = obj.load_feedback_info(0, 100)
    print(res)
from flask import Flask
import lc_git_stat
import datetime
import json
import mysql_service
from loghandle import logger

sql_service = mysql_service.mysqlService()


app = Flask(__name__)

@app.route('/user_info')
def get_user_info():
   td = datetime.date.today()
   yd = td + datetime.timedelta(days = -1)
   data = sql_service.load_user_daily_info(str(td))
   if len(data) == 0:
      data = sql_service.load_user_daily_info(str(yd))
   info = []
   for u in data:
      line = []
      for item in data[u]:
         line.append(str(item))
      info.append(line)
   # logger.info(info)
   return json.dumps(info)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=810)
   #app.run(host='127.0.0.1', port=810)

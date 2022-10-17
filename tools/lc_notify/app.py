from flask import Flask
import lc_git_stat
import datetime
import json


app = Flask(__name__)

@app.route('/user_info')
def get_user_info():
   td = datetime.date.today()
   info = lc_git_stat.stat_git_info2(td)
   return json.dumps(info)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=810)
   #app.run(host='127.0.0.1', port=810)

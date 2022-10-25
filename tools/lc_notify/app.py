from flask import Flask
from flask import request
import datetime
import json
import mysql_service
import lc_service
from loghandle import logger
import settings

sql_service = mysql_service.MysqlService()

# 访问leetcode官方接口的对象
leetcode_service = lc_service.LeetcodeService()

app = Flask(__name__)

@app.route('/user_info')
def get_user_info():
   td = datetime.date.today()
   yd = td + datetime.timedelta(days = -1)
   data = sql_service.load_all_user_daily_info_by_day(str(td))
   if len(data) == 0:
      data = sql_service.load_all_user_daily_info_by_day(str(yd))
   info = []
   for u in data:
      line = []
      tmplist = list(data[u])
      lazydays = tmplist[7]
      if lazydays >= len(settings.lazyLevels):
         tmplist[7] = settings.lazyLevels[-1]
      else:
         tmplist[7] = settings.lazyLevels[lazydays]
      for item in tmplist:
         line.append(str(item))
      info.append(line)
   # 按今日刷题量进行排序
   info = sorted(info, key=lambda item: int(item[6]), reverse=True)
   # logger.info(info)
   return json.dumps(info)


@app.route('/submit_account_info')
def submit_account_info():
   ret = ['0', "succ"]
   body = request.values
   logger.info(body)
   lc_account = body.get('lc_account')
   git_account = body.get('git_account')
   email = body.get('email_account')
   if email != '' and '@' not in email:
      ret[0] = '1'
      ret[1] = "邮箱格式错误!!!!"
      return json.dumps(ret)
   info = leetcode_service.get_user_lc_stat_info(lc_account)
   if not info:
      ret[0] = '1'
      ret[1] = "leetcode 账户不存在"
      return json.dumps(ret)
   userinfo = sql_service.search_account(lc_account)
   if not userinfo:
      logger.info("add lc_account: " + lc_account)
      sql_service.add_account_info(lc_account, git_account, email)
   else:
      u_email = userinfo[4]
      u_git = userinfo[1]
      user = userinfo[0]
      if lc_account != '' and email == '' and git_account == '':
         ret[0] = '1'
         ret[1] = '账户已经存在!!!'
         return json.dumps(ret)
      if (u_email != '' and email != '') or (u_git != '' and git_account != ''):
         ret[0] = '1'
         ret[1] = '邮箱或者git账户已经存在，如要更改请联系管理员!!!'
         return json.dumps(ret)
      if u_email == '' and email != '':
         logger.info(lc_account + " update email: " + email)
         sql_service.update_user_email(lc_account, email)
      if u_git == '' and git_account != '':
         logger.info(lc_account + " update git_account: " + git_account)
         sql_service.update_user_git_account(lc_account, git_account)
   
   return json.dumps(ret)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=810)
   #app.run(host='127.0.0.1', port=810)

#coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loghandle import logger
import settings

class EmailService(object):
    def __init__(self, user_emails):
        self.fm_addr = '595949643@qq.com'
        self.pass_wd = 'zeichyzgngnlbche'
        self.user_emails = user_emails
       
    def send_email(self, user, medal_type, award_flag):
        """
        user: 待接受邮件的用户
        medal_type: 奖励类型
        award_flag: 标记是否让收件人提供快递信息
        """
        if user not in self.user_emails:
            return False
        to_addr = self.user_emails[user]
        ret = True
        try:
            msg = MIMEMultipart()
            bodystr = "恭喜你，"
            if medal_type == settings.MedalType.Knight:
                bodystr += "上Knight了!!!"
            elif medal_type == settings.MedalType.Guardian:
                bodystr += "上Guardian了!!!"
            elif medal_type == settings.MedalType.CodeSubmit:
                bodystr += "push代码提交超过1000行了!!!"
            elif medal_type == settings.MedalType.ProblemSubmit:
                bodystr += "push题量超过50题了!!!"
            elif medal_type == settings.MedalType.ContinueDays:
                bodystr += "连续打卡超过100天了!!!"
            if award_flag:
                bodystr += "\n 为了表示鼓励，有一份小礼物要送给你，辛苦填写一下快递地址，收件人信息和电话号码～ \
                    回复此邮件即可!!\n 请放心，所有信息会严格保密。"
            msg.attach(MIMEText(bodystr, 'plain', 'utf-8'))
            msg['Subject'] = "leetcode刷题通知！"
            msg['From'] = self.fm_addr
            msg['To'] = to_addr
            smtp = smtplib.SMTP_SSL("smtp.qq.com")
            # 登录，需要：登录邮箱和授权码
            smtp.login(user=self.fm_addr, password=self.pass_wd)
            smtp.sendmail(self.fm_addr, to_addr, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            smtp.quit()  # 关闭连接
        except Exception as e:
            logger.error(e)
            ret = False
        return ret


if __name__ == '__main__':
    obj = EmailService(settings.emails)
    user = 'smilecode-2'
    obj.send_email(user, 4, 1)

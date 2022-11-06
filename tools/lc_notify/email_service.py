# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loghandle import logger
import settings


class EmailService(object):
    def __init__(self):
        self.fm_addr = '595949643@qq.com'
        self.pass_wd = 'zeichyzgngnlbche'

    def send_email(self, to_addr, bodystr):
        """
        to_addr: 待接受邮件的地址
        bodystr: 邮件内容
        """
        ret = True
        try:
            msg = MIMEMultipart()
            msg.attach(MIMEText(bodystr, 'plain', 'utf-8'))
            msg['Subject'] = "leetcode刷题通知！"
            msg['From'] = self.fm_addr
            msg['To'] = to_addr
            smtp = smtplib.SMTP_SSL("smtp.qq.com")
            # 登录，需要：登录邮箱和授权码
            smtp.login(user=self.fm_addr, password=self.pass_wd)
            # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            smtp.sendmail(self.fm_addr, to_addr, msg.as_string())
            smtp.quit()  # 关闭连接
        except Exception as e:
            logger.error(e)
            ret = False
        return ret


if __name__ == '__main__':
    obj = EmailService(settings.emails)
    user = 'smilecode-2'
    # obj.send_email(user, 4, 1)
    to_addr = "595949643@qq.com"
    bodystr = "sdfjkgjkh"
    obj.send_email2(to_addr, bodystr)

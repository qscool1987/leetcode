# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loghandle import logger
import settings


class EmailService(object):
    fm_addr = '595949643@qq.com'
    pass_wd = 'keyrfqxvnuribdce'

    @classmethod
    def send_email(cls, to_addr, bodystr):
        """
        to_addr: 待接受邮件的地址
        bodystr: 邮件内容
        """
        ret = True
        try:
            msg = MIMEMultipart()
            msg.attach(MIMEText(bodystr, 'plain', 'utf-8'))
            msg['Subject'] = "leetcode刷题通知！"
            msg['From'] = EmailService.fm_addr
            msg['To'] = to_addr
            smtp = smtplib.SMTP_SSL("smtp.qq.com")
            # 登录，需要：登录邮箱和授权码
            smtp.login(user=EmailService.fm_addr,
                       password=EmailService.pass_wd)
            # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            smtp.sendmail(EmailService.fm_addr, to_addr, msg.as_string())
            smtp.quit()  # 关闭连接
        except Exception as e:
            logger.error(e)
            ret = False
        return ret

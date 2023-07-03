# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/6/26 10:14
@file    :mailOperation.py
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from common.util.fileOperation import get_file_name
from common.util.globalVars import GolStatic
from common.util.logOperation import logger


def send_mail(file: str, contents: str) -> None:
    """
    发送邮件
    :param file:
    :param contents:
    :return:
    """
    logger.info("本次发送邮件附件地址: {}".format(file))
    myConfig = GolStatic.get_pro_var('MYCONFIG')
    mail_config = dict(myConfig.get_items('MAIL'))
    # 设置服务器
    mail_host = eval(mail_config.get('mail_host')) or 'smtp.qq.com'
    # 发件人
    sender = eval(mail_config.get('sender')) or '2584167983@qq.com'
    # 发件人授权码而非邮箱密码
    sender_pass = eval(mail_config.get('sender_pass')) or 'jctcwqoxyisuebaa'
    # 收件人
    receivers = eval(mail_config.get('receivers')) or ['lyh2584167983@163.com']
    # 邮件主题
    subject = mail_config.get('subject') or 'auto test report'
    # 邮件内容
    content = mail_config.get('content') or '请查收'

    # 创建一个带附件的实例
    msg = MIMEMultipart()
    # 邮件主题
    msg["Subject"] = subject
    msg["From"] = sender
    # 多个收件人，可用join连接
    msg["To"] = ','.join(receivers)

    # ---文字部分---
    part = MIMEText(content + contents)
    msg.attach(part)

    # ---附件部分---
    filename = get_file_name(file)
    part = MIMEApplication(open(file, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(part)

    logger.info("发件人: >>>{}".format(sender))
    logger.info("收件人: >>>{}".format(receivers))
    logger.info("邮件内容: >>>{}".format(content))
    logger.info("附件名称: >>>{}".format(filename))
    try:
        # 连接smtp邮件服务器,端口默认是25
        mail = smtplib.SMTP(mail_host, timeout=30)
        # 登陆服务器
        mail.login(sender, sender_pass)
        # 发送邮件
        mail.sendmail(sender, receivers, msg.as_string())
        mail.close()
        logger.info("发送邮件成功!")
    except Exception as e:
        logger.error("发送邮件失败: >>>{}".format(e))
        raise e


if __name__ == '__main__':
    ...

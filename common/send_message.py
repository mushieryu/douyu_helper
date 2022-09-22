# encoding:utf-8
import requests
import smtplib
from common.dirs import LOGS_DIR, LOG_FILE
from common.logger import logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from common.get_secrets import get_secrets
from common.config import conf

import re

def log_reader():
    with open(LOG_FILE, 'r', encoding="UTF-8") as lg:
        logs = lg.readlines()
        logs_str = ''.join(logs).replace("\n","\n\n")
    return logs_str


def send_message(send_key):
    url = "https://sctapi.ftqq.com/{}.send".format(send_key)
    data = {
        "title": u"DouYu-Helper执行结果",
        "desp": log_reader()
    }
    if data['desp']:
        try:
            logger.info("------执行server酱推送------")
            requests.post(url, data=data)
            logger.info("------推送成功------")
        except Exception as e:
            logger.error(e)
    else:
        data = {
            "title": u"DouYu-Helper执行结果",
            "desp": "执行出现问题,日志为空"
        }
        requests.post(url, data=data)

def mail_send(error):
    mode = int(conf.get_conf("SendMode")['mailsend'])
    if mode == 1:
        username = get_secrets('MAILSEND')
        password = get_secrets('PASSWORD')
        mail_from = username
        mail_to = get_secrets('MAILGET')
        mail_subject = "Github error"
        mail_body = error

        mimemsg = MIMEMultipart()
        mimemsg['From'] = mail_from
        mimemsg['To'] = mail_to
        mimemsg['Subject'] = mail_subject
        mimemsg.attach(MIMEText(mail_body, 'plain'))

        mimemsg = MIMEMultipart()
        mimemsg['From'] = mail_from
        mimemsg['To'] = mail_to
        mimemsg['Subject'] = mail_subject
        mimemsg.attach(MIMEText(mail_body, 'plain'))
        connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
        connection.starttls()
        connection.login(username, password)
        connection.send_message(mimemsg)
        connection.quit()

def bank_send(success, message):
    mode = int(conf.get_conf("SendMode")['banksend'])
    if mode == 1:
        title = success and '/GitHub Action Success' or 'GitHub Action Failure'
        barkurl = get_secrets('BARKURL')
        if barkurl.startswith('https'):
            requests.get(barkurl + '/' + title + '/' + message)

if __name__ == '__main__':
    send_message()
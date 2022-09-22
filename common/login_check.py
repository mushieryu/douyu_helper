# encoding:utf-8
from common.douyu_request import dyreq
from common.logger import logger
from common.send_message import mail_send, bank_send

Is_login = 0
login_url = "/wgapi/livenc/liveweb/follow/list"


def is_login():
    """
    :return:返回登陆结果,用于主程序判断
    """
    global Is_login
    login = dyreq.request("get", login_url).json()
    if login['error'] == 0:
        Is_login = 1
        logger.info("Cookie有效,登陆成功")
    else:
        logger.warning("登陆失败,请检查Cookie有效性")
        bank_send(False, '登陆失败,请检查Cookie有效性')
        mail_send('登陆失败,请检查Cookie有效性')
    return Is_login


if __name__ == '__main__':
    is_login()

# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/6/25 14:13
@file    :conftestpy
"""
import os
import time

import pytest

from common.core.mysqlConnection import MySqlConnect
from common.util.filePath import REPORT, CONFDIRENV
from common.util.fileZip import make_zip
from common.util.getConfig import MyConfig
from common.util.globalVars import GolStatic
from common.util.logOperation import logger
from common.util.mailOperation import send_mail


@pytest.fixture(scope="session")
def login_and_logout():
    # 登陆
    yield
    # 登出


def pytest_configure(config):
    """
    在测试配置阶段执行的钩子函数
    可以在这里对 pytest 配置进行修改或初始化操作
    :param config:
    :return:
    """
    # 注册自己编写的插件
    # config.pluginmanager.register(MyPlugin())
    pass


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    在测试会话开始前执行的钩子函数
    可以在这里执行一些准备工作，如创建临时目录、建立数据库连接等等
    :param session:
    :return:
    """
    # 启动多进程跑用例 或在py文件跑用例时，需要重新实例化MyConfig()
    # PROCONFIG = MyConfig()
    # GolStatic.set_pro_var('PROCONFIG', PROCONFIG)
    PROCONFIG = GolStatic.get_pro_var('PROCONFIG')
    # 实例化环境配置对象
    path = CONFDIRENV + PROCONFIG.get_config('ENVIRONMENT', 'ENV')
    MYCONFIG = MyConfig(path)
    GolStatic.set_pro_var('MYCONFIG', MYCONFIG)
    if MYCONFIG.get_config_bool('MYSQL', 'is_MySql'):
        # 连接数据库
        host = MYCONFIG.get_config('MYSQL', 'host')
        port = MYCONFIG.get_config('MYSQL', 'port')
        user = MYCONFIG.get_config('MYSQL', 'user')
        password = MYCONFIG.get_config('MYSQL', 'password')
        database = MYCONFIG.get_config('MYSQL', 'database')
        charset = MYCONFIG.get_config('MYSQL', 'charset')
        MYSQL = MySqlConnect(host=host, port=port, user=user, password=password, database=database, charset=charset)
        GolStatic.set_pro_var('MYSQL', MYSQL)


def pytest_collection_modifyitems(config, items):
    """
    在测试收集后执行的钩子函数
    可以访问和修改每个测试项目
    可以对测试项目列表进行重新排序，例如按名称排序
    :param config:
    :param items:
    :return:
    """
    pass


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session):
    """
    整个测试过程结束时执行一次。可以在此处实现清理工作
    例如：发送邮件
    :param session:
    :return:
    """
    # 生成allure报告
    cmd = 'allure generate --clean %s -o %s ' % (REPORT + '/xml', REPORT + '/html')
    os.system(cmd)
    myConfig = GolStatic.get_pro_var('MYCONFIG')
    # 打包报告文件放在historyReport目录下
    file = make_zip(REPORT)
    if myConfig.get_config_bool('MAIL', 'is_send_mail'):
        # 发送邮件
        send_mail(file)


def pytest_unconfigure(config):
    """
    在测试执行完毕后执行一在此处释放资源，例如删除临时文件等
    :param config:
    :return:
    """
    pass


def pytest_terminal_summary(terminalreporter):
    """
    收集测试结果
    注：启用多进程跑时，收集结果需要优化
    :param terminalreporter:
    :return:
    """
    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _DESELECTED = len([i for i in terminalreporter.stats.get("deselected", [])])
    _SELECTED = terminalreporter._numcollected - _DESELECTED
    _TIMES = time.time() - terminalreporter._sessionstarttime
    logger.info(f"用例总数: {_SELECTED}")
    logger.info(f"异常用例数: {_ERROR}")
    logger.info(f"失败用例数: {_FAILED}")
    logger.warning(f"跳过用例数: {_SKIPPED}")
    logger.info("用例执行时长: %.2f" % _TIMES + " s")

    try:
        _RATE = _PASSED / _SELECTED * 100
        logger.info("用例成功率: %.2f" % _RATE + " %")
    except ZeroDivisionError:
        logger.info("用例成功率: 0.00 %")

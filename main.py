# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/6/25 14:07
@file    :main.py
"""
import platform
import subprocess

import pytest

from common.util.filePath import REPORT, TESTCASE, ensure_path_sep
from common.util.getConfig import MyConfig
from common.util.globalVars import GolStatic
from common.util.logOperation import logger

if __name__ == '__main__':
    # 实例化框架配置对象
    PROCONFIG = MyConfig()
    GolStatic.set_pro_var('PROCONFIG', PROCONFIG)
    logger.info("main")
    if PROCONFIG.get_config_bool('PYTEST', 'is_gip'):
        # 启动多进程跑用例时，pytest_sessionstart需要重新实例化MyConfig()
        args_list = ['-vs', TESTCASE,
                     '--reruns', PROCONFIG.get_config('PYTEST', 'reruns'),
                     '--reruns-delay', PROCONFIG.get_config('PYTEST', 'delay'),
                     '--maxfail', PROCONFIG.get_config('PYTEST', 'maxfail'),
                     '-n', PROCONFIG.get_config('PYTEST', 'gip'),
                     '--dist=loadfile',
                     '--alluredir', ensure_path_sep(REPORT + '/xml'),
                     '--clean-alluredir',
                     '--disable-warnings']
    else:
        args_list = ['-vs', TESTCASE,
                     '--reruns', PROCONFIG.get_config('PYTEST', 'reruns'),
                     '--reruns-delay', PROCONFIG.get_config('PYTEST', 'delay'),
                     '--maxfail', PROCONFIG.get_config('PYTEST', 'maxfail'),
                     '--alluredir', ensure_path_sep(REPORT + '/xml'),
                     '--clean-alluredir',
                     '--disable-warnings']
    pytest.main(args_list)
    # if platform.system() == 'Windows':
    #     # 执行端口启动allure报告
    #     cmd = 'allure serve --port 8051 ' + ensure_path_sep(REPORT + '/xml')
    #     # 以子进程方式打开
    #     p = subprocess.Popen(cmd, shell=True)
    #     p.wait()

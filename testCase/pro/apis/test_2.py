# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/6/28 12:54
@file    :test_2.py
"""
import pytest

from common.core.assertData import check_resp
from common.core.reqSend import requestSend
from common.util.yamlOperation import read_folder_case


class TestExample:
    # 获取接口内容：
    # 方式一：通过读excel方式获取
    test_case = read_folder_case(r"E:\APIAutoTestModel\testData\pro\model")

    def test_1(self, login_and_logout):
        request = login_and_logout
        request_body = {"pageNumber": 10}
        result = requestSend(request, case=self.test_case.get('riskManageList'), request_body=request_body)
        assert check_resp(result, self.test_case.get('riskManageList').get('expected'))

    def test_2(self, login_and_logout):
        assert 1 == 1

    def test_3(self, login_and_logout):
        assert 1 == 1


if __name__ == '__main__':
    pass

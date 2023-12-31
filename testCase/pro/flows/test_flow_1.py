# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/7/3 14:53
@file    :test_flow_1.py
"""
import allure
import pytest

from common.core.assertData import check_resp
from common.core.reqSend import requestSend
from common.core.retryRequests import repeated_requests
from common.util.logOperation import logger
from common.util.yamlOperation import read_folder_case


@allure.epic('pro项目名称')
@allure.feature("业务流测试示例")
class TestFlowExample:
    # 获取接口内容：
    # 方式一：通过读excel方式获取
    test_case = read_folder_case(r"E:\APIAutoTestModel\testData\pro\model_1")
    count = 0

    @repeated_requests()
    def retry(self) -> bool:
        """
        请求重试示例
        :return: 返回False表示需重推, 返回True表示无需重推
        """
        if self.count == 3:
            return True
        else:
            return False

    @allure.story("示例一")
    def test_1(self, login_and_logout):
        request = login_and_logout
        # 执行第一个接口
        result = requestSend(request, case=self.test_case.get('step_1'))
        # 断言
        # 方式一：通过check_resp断言，默认部分匹配
        assert check_resp(result, self.test_case.get('riskManageList').get('expected'))

        # 参数化：
        # 方式四和方式五：通过指定接口的响应报文和请求报文的某个字段值进行参数化(详见step_2.yaml文件)
        # pageNumber: $Resp{step_1.isSuccess} pageNumber值为step_1接口的响应报文中isSuccess的值
        # pageSize: $Req{step_1.pageSize} pageSize值为step_1接口的请求报文中pageSize的值
        # 执行第二个接口
        result = requestSend(request, case=self.test_case.get('step_2'))
        # 断言
        # 方式一：通过check_resp断言，默认部分匹配
        assert check_resp(result, self.test_case.get('riskManageList').get('expected'))
        self.retry()


if __name__ == '__main__':
    pass

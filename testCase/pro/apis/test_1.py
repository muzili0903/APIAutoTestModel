# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/6/26 16:37
@file    :test_1.py
"""
import pytest

from common.core.assertData import check_resp, check_value
from common.core.reqSend import requestSend
from common.util.excelOperation import ReadExcel
from common.util.jsonOperation import read_json
from common.util.logOperation import logger


class TestExample:
    # 获取接口内容：
    # 方式一：通过读excel方式获取
    test_case = ReadExcel(filename=r'E:\APIAutoTestModel\testData\pro\APIAutoTestDataModel.xlsx').read_to_dict()

    # 参数化：
    # 方式一：通过json文件进行参数化，将json文件字段值替换掉请求报文字段值
    @pytest.mark.parametrize('kwargs',
                             read_json(r'E:\APIAutoTestModel\testData\proParams\model\riskManageList.json'))
    def test_1(self, login_and_logout, kwargs):
        logger.info(kwargs)
        request = login_and_logout
        result = requestSend(request, case=self.test_case.get('riskManageList'), request_body=kwargs)
        # 断言
        # 方式一：通过check_resp断言，默认部分匹配
        assert check_resp(result, self.test_case.get('riskManageList').get('expected'))

    def test_2(self, login_and_logout):
        request = login_and_logout
        # 参数化：
        # 方式二：自定义字段参数化
        request_body = {"pageNumber": 10}
        logger.info("test_2: {}".format(self.test_case.get('riskManageList')))
        result = requestSend(request, case=self.test_case.get('riskManageList'), request_body=request_body)
        # 断言
        # 方式二：通过check_value断言
        assert check_value(result.get('isSuccess'),
                           self.test_case.get('riskManageList').get('expected').get('isSuccess'))

    # 参数化：
    # 方式三：通过json文件进行参数化，将json文件字段值替换掉请求报文字段值，json文件存在多组报文
    @pytest.mark.parametrize('kwargs',
                             read_json(r'E:\APIAutoTestModel\testData\proParams\model\riskManageList_mutil.json'))
    def test_3(self, login_and_logout, kwargs):
        logger.info(kwargs)
        assert 1 == 1


if __name__ == '__main__':
    pass

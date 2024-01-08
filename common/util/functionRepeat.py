# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/12/15 10:44
@file    :functionRepeat.py
"""
from typing import Any


class FunctionRepeat(object):
    """
    需要重推的管理台内部接口: 示例
    """

    @staticmethod
    @repeated_requests()
    def queryResultSingleFieldValues(request: object, item: object, field_xpath: str, value: object,
                                     request_body: dict = None, **kwargs) -> Any:
        """
        查询响应结果中某个字段值(jsonpath取整个list值)与预期结果value是否相等, 不相等重推
        :param request:
        :param item:
        :param field_xpath: 响应结果的xpath表达式, 使用传进来的xpath获取到结果, 结束重推, 获取不到结果重推
        :param value: 需要校验的值
        :param request_body:
        :return:
        """
        pass


if __name__ == '__main__':
    pass
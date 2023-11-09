# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/11/9 14:53
@file    :check.py
"""
from resCheck.proApi import ProApi

class Check(ProApi):
    """
    在实现业务流程中，用到某个接口时，需要对该接口进行校验时，可在此类中实现对接口的校验，减少重复编写接口校验代码
    """

    def queryApi(response_body: list, expected_body: list, **kwargs) -> None:
        assert check_list(response_body, expected_body)

    def updateApi(response_body: list, expected_body: list, **kwargs) -> None:
        assert check_list(response_body, expected_body)

if __name__ == '__main__':
    ...

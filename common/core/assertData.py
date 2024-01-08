# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/6/25 17:39
@file    :assertData.py
"""
from datetime import datetime
from typing import Any

from common.util.logOperation import logger


def check_code(response_code: int, expect_code: int) -> bool:
    """
    校验响应码
    :param response_code:
    :param expect_code:
    :return:
    """
    logger.info("check_code: ")
    logger.info("respone_value: >>> {}".format(response_code))
    logger.info("expect_value: >>> {}".format(expect_code))
    if response_code != expect_code:
        logger.info("请求状态码校验不通过: 预期code: >>> {} 实际code: >>> {}".format(response_code, expect_code))
        return False
    return True


def check_value(respone_value: Any, expect_value: Any) -> bool:
    """
    校验值
    :param respone_value:
    :param expect_value:
    :return:
    """
    logger.info("check_value: ")
    logger.info("respone_value: >>> {}".format(respone_value))
    logger.info("expect_value: >>> {}".format(expect_value))
    try:
        if isinstance(expect_value, str):
            if expect_value.__ne__(str(respone_value)):
                return False
        elif isinstance(expect_value, int):
            if expect_value.__ne__(int(respone_value)):
                return False
        elif isinstance(expect_value, float):
            if expect_value.__ne__(float(respone_value)):
                return False
        else:
            if expect_value.__ne__(respone_value):
                return False
        return True
    except Exception as e:
        logger.error("值校验不一致: >>> {}".format(respone_value))
        logger.error("值校验报错: >>> {}".format(e))
        return False


def check_list(response_body: list, expected_body: list, checked_type: str = 'perfect_match') -> bool:
    """
    校验列表字段值
    :param response_body: 响应结果
    :param expected_body: 预期结果
    :param checked_type: 校验值的方式
    :return:
    """
    logger.info("check_list: ")
    logger.info("响应报文: >>> {}".format(response_body))
    logger.info("预期结果: >>> {}".format(expected_body))
    logger.info("校验方式: >>> {}".format(checked_type))

    result = list()
    if checked_type in ['perfect_match', '==']:
        if response_body.__len__() != expected_body.__len__():
            return False
    try:
        response_body.sort()
        expected_body.sort()
    except Exception as e:
        logger.error("'<' not supported between instances of 'dict' and 'int'")
        logger.error("list排序报错: >>> {}".format(e))
    try:
        for index, value in enumerate(expected_body):
            if isinstance(value, dict):
                result.append(check_resp(response_body[index], value, checked_type))
            elif isinstance(value, list):
                result.append(check_list(response_body[index], value, checked_type))
            else:
                result.append(check_value(response_body[index], value))
        else:
            if checked_type in ['perfect_match', '==']:
                if response_body.__len__() != expected_body.__len__():
                    return False
                else:
                    pass
    except Exception as e:
        logger.error("JSON格式校验, 预期结果: >>> {}与响应结果: >>> {}值不一致".format(expected_body, response_body))
        logger.error("值校验报错: >>> {}".format(e))
        return False
    if False not in result:
        return True
    return False


def check_resp(response_body: dict, expected_body: dict, checked_type: str = 'partial_match') -> bool:
    """
    校验响应报文，预期结果json文件格式
    :param response_body:
    :param expected_body:
    :param checked_type: 全校验: perfect_match, == 部分校验: partial_match or in
    :return:
    """
    logger.info("check_resp: ")
    logger.info("响应报文: >>> {}".format(response_body))
    logger.info("预期结果: >>> {}".format(expected_body))
    logger.info("校验方式: >>> {}".format(checked_type))

    if checked_type in ['perfect_match', '==']:
        if response_body.__len__() != expected_body.__len__():
            return False

    result = list()
    if isinstance(expected_body, dict):
        for key, value in expected_body.items():
            if key not in response_body:
                logger.info("JSON格式校验, 关键字: >>> {}不在响应结果: >>> {}中".format(key, response_body))
                return False
            else:
                if isinstance(value, dict) and isinstance(response_body.get(key), dict):
                    result.append(check_resp(response_body.get(key), value, checked_type))
                elif not isinstance(value, type(response_body.get(key))):
                    logger.info(
                        "JSON格式校验, 关键字: >>> {}预期结果: >>> {}与响应结果: >>> {}类型不符".format(key, value, response_body.get(key)))
                    return False
                else:
                    if isinstance(value, list):
                        result.append(check_list(response_body.get(key), value, checked_type))
                    else:
                        result.append(check_value(response_body.get(key), value))
    else:
        logger.info("JSON校验内容非dict格式: >>> {}".format(expected_body))
        return False
    if False not in result:
        return True
    return False


def check_one_to_many(response_body: list, expected_body: Any, is_date: bool = False) -> bool:
    """
    校验预期值与实际列表值全匹配, 适用于查询结果校验, 日期模糊匹配
    :param response_body:
    :param expected_body:
    :param is_date: 是否日期校验
    :return:
    """
    logger.info("check_one_to_many: ")
    logger.info("响应报文: >>> {} 响应报文类型: >>> {}".format(response_body, type(response_body)))
    logger.info("预期结果: >>> {} 预期结果类型: >>> {}".format(expected_body, type(expected_body)))
    logger.info("校验方式: >>> perfect_match")

    if isinstance(response_body, list):
        result = list()
        for response in response_body:
            if not is_date:
                if str(response) != str(expected_body):
                    result.append(False)
                    break
            else:
                if len(expected_body[0]) in (8, 10):
                    start_time = datetime.strptime(expected_body[0], '%Y-%m-%d')
                else:
                    start_time = datetime.strptime(expected_body[0][0: len(expected_body[0])] + ' 0:0:0',
                                                   '%Y-%m-%d %H:%M:%S')
                # 结束日期加上 23:59:59
                end_time = datetime.strptime(expected_body[1][0: len(expected_body[1])] + ' 23:59:59',
                                             '%Y-%m-%d %H:%M:%S')
                if len(response) in (19, 17):
                    response_time = datetime.strptime(response, '%Y-%m-%d %H:%M:%S')
                elif len(response) in (10, 8):
                    response_time = datetime.strptime(response, '%Y-%m-%d')
                else:
                    result.append(False)
                    break
                if response_time < start_time or response_time > end_time:
                    result.append(False)
                    break
        return all(result)
    else:
        logger.info("JSON校验内容非list格式: >>> {}".format(response_body))
        return False


if __name__ == '__main__':
    ...

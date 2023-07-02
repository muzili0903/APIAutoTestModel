# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/1 13:41
@Auth ： muzili
@File ： jsonOperation.py
@IDE  ： PyCharm
"""
import json
import os

from common.util.logOperation import logger


def read_json(file, is_str=False):
    """
    读取json文件内容
    :param file:
    :param is_str: 为False时返回dict
    :return: 默认返回dict
    """
    if not os.path.exists(file):
        logger.error("文件不存在, 获取数据失败: >>>{}".format(file))
        return None
    with open(file=file, encoding='utf-8') as f:
        content = json.load(f)
    if is_str:
        return str(content)
    else:
        return content


if __name__ == '__main__':
    print(read_json(r'E:\project\APIAutoTestModel\testData\proParams\model\riskManageList.json'))
    pass

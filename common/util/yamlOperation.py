# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/6/26 10:06
@file    :yamlOperation.py
"""
import os
from typing import Any
from filelock import FileLock

import yaml

from common.util.fileOperation import get_all_file, get_file_name
from common.util.logOperation import logger


def read_yaml(file: str, is_str: bool = True) -> Any:
    """
    读取yaml文件内容
    :param file:
    :param is_str: 为False时返回dict
    :return: 默认返回str
    """
    if not os.path.exists(file):
        logger.error("文件不存在, 获取数据失败: >>>{}".format(file))
        return None
    with FileLock(str(path) + ".lock"):
        with open(file=file, encoding='utf-8') as f:
            content = yaml.load(f, yaml.FullLoader)
    if is_str:
        return str(content)
    return content


def write_yaml(file: str, obj: object) -> None:
    """
    将python对象写入yaml文件
    :param file:
    :param obj:
    :return:
    """
    # sort_keys=False字段表示不改变原数据的排序
    # allow_unicode=True 允许写入中文，必须以字节码格式写入
    path = os.path.split(file)[0]
    if not os.path.exists(path):
        os.makedirs(path)
    with FileLock(str(path) + ".lock"):
        with open(file=file, mode="w", encoding='utf-8') as f:
            yaml.dump(data=obj, stream=f, sort_keys=False, allow_unicode=True)


def read_folder_case(path: str) -> dict:
    """
    读取某个目录下的yaml, 以文件名为key, 文件内容为value的形式返回
    :param path:
    :return:
    """
    if not os.path.exists(path):
        logger.error("目录不存在, 获取数据失败: >>>{}".format(path))
        return dict()
    path_list = get_all_file(path)
    cases = dict()
    for path in path_list:
        filename = get_file_name(path).split('.')[0]
        data = read_yaml(path, is_str=False)
        cases.update({filename: data})
    return cases


if __name__ == "__main__":
    ...

# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/6/26 10:17
@file    :fileOperation.py
"""
import os

from common.util.filePath import ensure_path_sep
from common.util.logOperation import logger


def get_all_file(path: str) -> list:
    """
    获取目录下的所有文件路径
    :param path:
    :return:
    """
    files_path = []
    try:
        files = os.listdir(path)
        for f in files:
            f_path = ensure_path_sep(os.path.join(path, f))
            files_path.append(f_path)
    except FileNotFoundError:
        logger.error("找不到指定的文件路径: >>>{}".format(path))
    except NotADirectoryError:
        logger.error("目录名称无效: >>>{}".format(path))
    return files_path


def get_file_name(path: str) -> str:
    """
    获取文件名字
    :param path:
    :return:
    """
    return os.path.split(path)[1]


def get_file_path(path: str) -> str:
    """
    获取文件所在路径
    :param path:
    :return:
    """
    return os.path.split(path)[0]


if __name__ == '__main__':
    ...

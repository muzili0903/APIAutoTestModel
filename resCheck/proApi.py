# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/11/9 14:53
@file    :pro.py
"""

from abc import ABCMeta, abstractmethod


class ProApi(metaclass=ABCMeta):
    """
    pro项目接口校验
    """

    @abstractmethod
    def queryApi(self, *args, **kwargs): ...

    @abstractmethod
    def updateApi(self, *args, **kwargs): ...

if __name__ == '__main__':
    ...

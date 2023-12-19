# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/6/26 11:14
@file    :retryRequests.py
"""
from typing import Callable, Any
import threading
import time

from common.util.globalVars import GolStatic
from common.util.logOperation import logger
from functools import wraps

proConfig = GolStatic.get_pro_var('PROCONFIG')
retry_number = proConfig.get_config_int('RETRY', 'number')
sleeptime = proConfig.get_config_int('RETRY', 'sleeptime')


class MyThread(threading.Thread):
    def __init__(self, func, *args, **kwargs):
        super(MyThread, self).__init__()
        self.result = None
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.result = self.func(*self.args, **self.kwargs)

    def get_result(self):
        threading.Thread.join(self)  # 等待线程执行完毕
        try:
            return self.result
        except Exception:
            return None


def repeated_requests(isRetryNumberError: bool = True) -> Any:
    """
    被装饰的函数func返回值必须是bool类型
    :param isRetryNumberError:
    :return:
    """

    def wrapper(func: Callable):

        @wraps(func)
        def inner(*args, **kwargs):
            logger.info('进入wrapper')
            thr = MyThread(func, *args, **kwargs)
            funcQueue.put(thr)
            count_func = {func: 1}
            result = None
            while not funcQueue.empty():
                function = funcQueue.get(True, .5)
                function.start()
                result = function.get_result()
                logger.info('wrapper result: {}'.format(result))
                if result is None:  # 被装饰的函数func返回None或断言失败,抛出断言失败让pytest捕获
                    raise AssertionError('断言失败或返回None')
                if not result:  # 被装饰的函数func返回False,重推
                    if count_func.get(func).__eq__(retry_number):  # 限制重推次数
                        if isRetryNumberError:
                            logger.error("isRetryNumberError值为: {}, 超过重推次数抛异常, 用例失败".format(isRetryNumberError))
                            raise AssertionError('超过重推次数抛异常')
                        else:
                            logger.info("isRetryNumberError值为: {}, 超过重推次数不会抛异常, 用例继续执行".format(isRetryNumberError))
                            return result
                    logger.info('再次进入wrapper')
                    time.sleep(sleeptime)
                    thr = MyThread(func, *args, **kwargs)
                    funcQueue.put(thr)
                    count_func[func] += 1
            return result

        return inner

    return wrapper


if __name__ == '__main__':
    pass

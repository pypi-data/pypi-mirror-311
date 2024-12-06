#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2024/11/28 15:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from meutils.async_task import worker
from meutils.async_task.tasks import test
from celery.result import AsyncResult


# print(worker.conf)

# @shared_task(
#     autoretry_for=(Exception,),      # 自动重试的异常类型
#     retry_kwargs={
#         'max_retries': 3,            # 最大重试次数
#         'countdown': 60              # 重试等待时间（秒）
#     },
#     retry_backoff=True,              # 启用指数退避
#     retry_backoff_max=600,           # 最大退避时间（秒）
#     retry_jitter=True                # 添加随机抖动
# )
# def my_task():
#     try:
#         # 任务逻辑
#         result = some_operation()
#         return result
#     except Exception as exc:
#         logger.error(f"Task failed: {exc}")
#         raise  # 触发自动重试


if __name__ == '__main__':
    r = test.do_sync_task.apply_async(kwargs={'a': 1, 'b': 2})
    logger.debug(r.backend)
    # test.ado_sync_task.apply_async(kwargs={'a': 1, 'b': 2})

    # print(AsyncResult(r.id).result)
    # result.backend


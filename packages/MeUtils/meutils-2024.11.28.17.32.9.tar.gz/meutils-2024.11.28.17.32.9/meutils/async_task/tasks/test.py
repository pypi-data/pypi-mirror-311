#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kling
# @Time         : 2024/11/28 16:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.decorators.retry import retrying

from meutils.async_task import worker, shared_task


@shared_task
def do_sync_task(**kwargs):
    logger.debug("同步任务")
    return kwargs


@shared_task()
async def do_sync_task(**kwargs):
    logger.debug("同步任务+协程")
    return kwargs


@shared_task
@retrying(3)
def proxy_task(**kwargs):
    method = kwargs.pop('method', '')
    url = kwargs.pop('url', '')

    logger.debug(kwargs)

    response = requests.request(method, url, **kwargs).json()

    return response

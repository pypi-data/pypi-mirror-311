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
from meutils.async_utils import async_to_sync_pro
from meutils.async_task import worker, shared_task


@shared_task
def do_sync_task(sleep=10, **kwargs):
    logger.debug("同步任务")
    time.sleep(sleep)

    return kwargs


# AttributeError: 'AsyncToSync' object has no attribute '__name__'. Did you mean: '__ne__'?


# @shared_task(name='meutils.async_task.tasks.test.proxy_task')
@shared_task
@async_to_sync_pro
async def ado_sync_task(**kwargs):
    logger.debug("同步任务+协程")
    await asyncio.sleep(10)
    return kwargs


class Request(BaseModel):
    method: str = "GET"
    url: str = "https://api.chatfire.cn/"


@worker.task(pydantic=True)
def do_pydantic_task(request: Request):
    return request


@shared_task
@retrying(3)
def proxy_task(**kwargs):
    method = kwargs.pop('method', '')
    url = kwargs.pop('url', '')

    logger.debug(kwargs)

    response = requests.request(method, url, **kwargs).json()

    return response


if __name__ == '__main__':
    # print(do_sync_task.apply_async(kwargs={'a': 1, 'b': 2}))
    print(AsyncToSync)

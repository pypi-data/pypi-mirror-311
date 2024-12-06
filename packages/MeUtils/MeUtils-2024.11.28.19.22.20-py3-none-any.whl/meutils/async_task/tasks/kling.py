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
async def do_task(**kwargs):
    return kwargs


@shared_task
@retrying(3)
async def proxy_task(**kwargs):
    pass

    return response

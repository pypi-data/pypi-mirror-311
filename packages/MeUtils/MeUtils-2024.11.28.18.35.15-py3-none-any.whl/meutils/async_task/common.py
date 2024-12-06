#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2024/11/28 15:28
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.async_task import celery_config

from celery import Celery, Task, shared_task, states


class RetryableTask(Task):  # 实际上 在具体任务支持 执行重试就行
    """shared_task(base=RetryableTask)"""

    # 使用 tenacity 进行更灵活的重试控制
    @retrying(
        max_retries=6,
        title="Celery 任务重试"
    )
    def run_with_retry(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.run_with_retry(*args, **kwargs)


worker = Celery()

worker.config_from_object(celery_config)

worker.conf.update(
    # result_expires=30 * 24 * 60 * 60,
    # enable_utc=False,
    # timezone='Asia/Shanghai',
    task_track_started=True,
)

if __name__ == '__main__':
    print(worker.conf.humanize(with_defaults=False))

    print(worker.conf.broker_url)
    print(worker.conf.result_backend)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : model_info
# @Time         : 2024/11/21 15:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.schemas.oneapi._types import ModelGroupInfo, ModelInfo

ModelInfos = [
    {
        "ai-search": ModelInfo(
            icon="https://registry.npmmirror.com/@lobehub/assets-emoji-anim/1.0.0/files/assets/cowboy-hat-face.webp",
            note="AI搜索",
            tags="搜索",
            group="chatfire"
        ),
    },
    {
        "ai-search": ModelInfo(
            icon="https://registry.npmmirror.com/@lobehub/assets-emoji-anim/1.0.0/files/assets/cowboy-hat-face.webp",
            note="AI搜索",
            tags="搜索",
            group="chatfire"
        ),
    }
]

ModelGroupInfos = [
    {
        "chatfire": ModelGroupInfo(
            name="火宝",
            desc="火宝AI，国内领先的API厂商",
            icon="https://registry.npmmirror.com/@lobehub/assets-emoji-anim/1.0.0/files/assets/cowboy-hat-face.webp",
            notice="https://api.chatfire.cn/docs"
        )
    },
]

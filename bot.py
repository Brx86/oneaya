#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   bot.py
@Time    :   2022/05/24 17:39:43
@Author  :   Ayatale 
@Version :   1.1
@Contact :   ayatale@qq.com
@Github  :   https://github.com/brx86/
@Desc    :   My asynchronous bot based on nonebot2
"""


import os, nonebot
from typing import Any, Optional
from nonebot.adapters.onebot.v11 import Adapter

PATH = os.path.dirname(os.path.abspath(__file__))
nonebot.init()


class PatchedAdapter(Adapter):
    @classmethod
    def json_to_event(cls, json_data: Any, self_id: Optional[str] = None):
        if isinstance(json_data, dict) and json_data.get("post_type") == "message_sent":
            json_data["post_type"] = "message"
        return super().json_to_event(json_data, self_id)


driver = nonebot.get_driver()
driver.register_adapter(PatchedAdapter)
nonebot.load_plugins("plugins")

if __name__ == "__main__":
    nonebot.logger.warning("Hello Ayatale!")
    nonebot.run(app="__mp_main__:app")
    # nonebot.run()

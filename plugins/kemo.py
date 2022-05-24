from random import randint
from time import time
from typing import List

from nonebot import on_command, on_shell_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ShellCommandArgv
from nonebot.plugin import on
from nonebot.rule import ArgumentParser, command

kemo = on_command("kk")


@kemo.handle()
async def handle_kemo(matcher: Matcher):
    await matcher.send(Message("Kemomimi酱来了!"))
    await matcher.finish(
        MessageSegment.image(
            f"https://ayatale.coding.net/p/picbed/d/kemo/git/raw/master/{randint(1,696)}.jpg"
        )
    )

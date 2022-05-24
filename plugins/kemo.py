from random import randint

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher

kemo = on_command("kk")


@kemo.handle()
async def handle_kemo(matcher: Matcher):
    await matcher.send("Kemomimi酱来了!")
    await matcher.finish(
        MessageSegment.image(
            f"https://ayatale.coding.net/p/picbed/d/kemo/git/raw/master/{randint(1,696)}.jpg"
        )
    )

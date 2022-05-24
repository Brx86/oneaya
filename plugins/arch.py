from typing import List
from .aiorun import run

from nonebot import on_shell_command
from nonebot.adapters.onebot.v11 import Event, Message
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import ShellCommandArgv

arch = on_shell_command("arch")


@arch.handle()
async def handle_arch(
    matcher: Matcher, event: Event, args: List[str] = ShellCommandArgv()
):
    logger.warning(f"「sender」: {event.get_user_id()}")
    await matcher.send(Message("Start!"))
    if event.get_user_id() == "1239504152":
        result = await run(f"pacman -F {args[-1]}")
        await matcher.send(Message(result))
    await matcher.finish(Message("Finished!"))

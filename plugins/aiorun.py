import asyncio
from nonebot.log import logger


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    logger.warning(f"Running command: {cmd}")
    stdout, stderr = await proc.communicate()
    logger.error(f"[{cmd!r} exited with {proc.returncode}]")
    if stdout:
        return stdout.decode()
    if stderr:
        logger.warning(f"[stderr]\n{stderr.decode()}")

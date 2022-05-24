import asyncio
from nonebot.log import logger


async def aiorun(cmd, shell=True):
    proc = (
        await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        if shell
        else await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    )
    logger.warning(f"Running command: {cmd}")
    stdout, stderr = await proc.communicate()
    if stdout:
        return stdout.decode()
    if proc.returncode:
        logger.error(f"[{cmd!r} exited with {proc.returncode}]")
        if stderr:
            logger.warning(f"[stderr]\n{stderr.decode()}")


async def silicon(text, lang="bash", rp=False):
    from aiofiles import open

    async with open(f"/tmp/text", "w") as f:
        text = text.replace("'", "’").replace('"', "’") if rp else text
        textlist = text.splitlines()
        text = text if len(textlist) < 100 else "\n".join(textlist[:100])
        await f.write(text + "......")
    cmd = f"silicon /tmp/text -o/tmp/text.png -l{lang} -fLXGWWenKaiMono -b#000000 --no-window-controls"
    await aiorun(cmd)
    return "file:///tmp/text.png"

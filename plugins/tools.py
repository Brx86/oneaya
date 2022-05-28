import asyncio
from nonebot.log import logger
from nonebot.adapters import Bot, Event


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


async def pastebin(text, api=0, lang="sh"):
    import httpx
    from io import BytesIO

    pastebin_api = [
        "https://fars.ee/?u=1",
        "https://api.inetech.fun/clip?return=preview",
    ]
    async with httpx.AsyncClient() as client:
        r = await client.post(
            pastebin_api[0],
            files={"c": BytesIO(text.encode())},
        )
        if r.status_code == 200:
            return f"{r.text.strip()}/{lang}" if api == 0 else r.text.strip()


async def async_checker(bot: Bot, event: Event) -> bool:
    return True

import re, httpx
from typing import List

from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import ShellCommandArgv
from nonebot.plugin import on_shell_command

from .tools import aiorun, silicon, pastebin

arch = on_shell_command("arch")


desc = {
    "软件库": "仓库",
    "名字": "包名",
    "版本": "版本",
    "下载大小": "大小",
    "描述": "描述",
    "依赖于": "依赖",
    "维护者": "维护者",
    "得票": "得票",
    "URL": "上游",
    "打包者": "打包者",
    "编译日期": "编译日期",
    "AUR URL": "AUR链接",
    "首次提交": "首次提交",
    "最后修改": "最后修改",
}
desc_dep = {
    "依赖于": "依赖",
    "生成依赖": "构建依赖",
    "可选依赖": "可选依赖",
    "检查依赖": "检查依赖",
}


def safename(text):
    return re.sub(r"[^a-zA-Z0-9\+_.-]", "", text)


async def search(pkg, aur=False, dep=False):
    msg = ""
    pkg = safename(pkg)
    cmd = f"paru -Sai {pkg}" if aur else f"paru -Si {pkg}"
    result = await aiorun(cmd)
    if result is None:
        return
    logger.warning(result)
    dic = desc_dep if dep else desc
    for k, v in dic.items():
        partten = re.compile(f"{k}(.*?): (.*?)\n")
        info = partten.findall(result)
        if info:
            msg += f"{v}: {info[0][1]}\n"
    return msg.strip()


async def fuzzy_search(pkg):
    pkg = safename(pkg)
    cmd = f"paru -Ss {pkg} --limit 5"
    result = await aiorun(cmd)
    if result:
        picpath = await silicon(result, rp=True)
        return MessageSegment.image(picpath)
    else:
        return "请输入正确的包名"


async def get_pkgbuild(pkgname):
    async with httpx.AsyncClient() as client:
        api_url = f"https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD"
        r = await client.get(api_url, params={"h": pkgname})
        if r.status_code == 200:
            return await pastebin(r.text)


@arch.handle()
async def handle_arch(
    matcher: Matcher,
    # event: Event,
    args: List[str] = ShellCommandArgv(),
):
    if len(args) == 0:
        await matcher.finish(
            "注意：\n此插件可用于查询包名的详细信息\n用法:\n #arch <包名> 查询全部仓库\n #arch -a <包名> 仅查询aur\n #arch -Ss <包名> 模糊查询包名\n #arch -d/da <包名> 显示依赖\n #arch -Fl <包名> 显示包的文件内容\n #arch -L <包组名> 显示包组内容\n #arch -D <包名> 显示下载地址\n #arch -P <包名> 显示PKGBUILD\n #arch -Sy pacman -Sy\n #arch -Syy pacman -Syy"
        )
    if args[0] == "-a":
        msg = await search(args[1], aur=True)
    elif args[0] == "-d":
        msg = await search(args[1], dep=True)
    elif args[0] == "-da":
        msg = await search(args[1], aur=True, dep=True)
    elif args[0] == "-D":
        pkg = safename(args[1])
        result = await aiorun(f"pacman -Spdd {pkg}")
        msg = f"{pkg}下载地址:\n{result}" if result else "请输入正确的包名"
    elif args[0] == "-L":
        pkg = safename(args[1])
        result = await aiorun(f"pacman -Sgq {pkg}")
        msg = pastebin(result) if result else "请输入正确的包名"
    elif args[0] == "-Fl":
        pkg = safename(args[1])
        result = await aiorun(f"pacman -Fl {pkg}")
        msg = pastebin(result) if result else "请输入正确的包名"
    elif args[0] == "-P":
        pkg = safename(args[1])
        msg = await get_pkgbuild(pkg)
    else:
        msg = await search(args[0])
        if not msg:
            await matcher.send("未找到此包名，正在模糊搜索...")
            msg = await fuzzy_search(args[0])
    if msg:
        await matcher.finish(msg)
    await matcher.finish("请输入正确的包名")

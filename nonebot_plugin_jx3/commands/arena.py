"""commands/arena.py — JJC战绩/排行/统计指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter, get_server
from ..api_client import api_client, JX3APIError
from ..render import renderer
from ..database import db


# ===== JJC 战绩 =====
cmd_jjc = on_command("jjc", rule=group_filter(), priority=5, block=True)


@cmd_jjc.handle()
async def handle_jjc(event: GroupMessageEvent, args: Message = CommandArg()):
    text = args.extract_plain_text().strip()
    parts = text.split()

    mode = 33  # 默认3v3
    server = None
    name = None

    if len(parts) == 3:
        # jjc 33 服务器 角色名
        try:
            mode = int(parts[0])
        except ValueError:
            pass
        server = parts[1]
        name = parts[2]
    elif len(parts) == 2:
        # jjc 33 角色名 或 jjc 服务器 角色名
        try:
            mode = int(parts[0])
            name = parts[1]
        except ValueError:
            server = parts[0]
            name = parts[1]
    elif len(parts) == 1:
        name = parts[0]
    else:
        await cmd_jjc.finish("格式：jjc [模式] [服务器] <角色名>\n示例：jjc 33 绝代天骄 赤瞳竹")

    if not server:
        if hasattr(event, "group_id"):
            server = await db.get_server(event.group_id)
        if not server:
            await cmd_jjc.finish("请先绑定服务器或指定服务器名")

    try:
        data = await api_client.arena_recent(server=server, name=name, mode=mode)
    except JX3APIError as e:
        await cmd_jjc.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("arena.html", title=f"⚔️ 名剑战绩 · {name}", data=data, mode=mode)
    await cmd_jjc.finish(MessageSegment.image(img))


# ===== JJC 排行 =====
cmd_jjc_rank = on_command("jjc排行", rule=group_filter(), priority=5, block=True)


@cmd_jjc_rank.handle()
async def handle_jjc_rank(event: GroupMessageEvent, args: Message = CommandArg()):
    text = args.extract_plain_text().strip()
    mode = 33
    if text:
        try:
            mode = int(text)
        except ValueError:
            pass

    try:
        data = await api_client.arena_awesome(mode=mode)
    except JX3APIError as e:
        await cmd_jjc_rank.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"🏆 名剑排行 · {mode}v{mode}", data=data)
    await cmd_jjc_rank.finish(MessageSegment.image(img))


# ===== JJC 统计 =====
cmd_jjc_stats = on_command("jjc统计", rule=group_filter(), priority=5, block=True)


@cmd_jjc_stats.handle()
async def handle_jjc_stats(event: GroupMessageEvent, args: Message = CommandArg()):
    text = args.extract_plain_text().strip()
    mode = 33
    if text:
        try:
            mode = int(text)
        except ValueError:
            pass

    try:
        data = await api_client.arena_schools(mode=mode)
    except JX3APIError as e:
        await cmd_jjc_stats.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"📊 名剑统计 · {mode}v{mode}", data=data)
    await cmd_jjc_stats.finish(MessageSegment.image(img))

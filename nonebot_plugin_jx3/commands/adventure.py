"""commands/adventure.py — 奇遇全系列指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter, get_server
from ..api_client import api_client, JX3APIError
from ..render import renderer
from ..database import db


async def _get_server_for_role(event, args: Message):
    """获取服务器（角色类查询的通用解析）"""
    if hasattr(event, "group_id"):
        server = await db.get_server(event.group_id)
        if server:
            return server
    from ..config import plugin_config
    if plugin_config.jx3_default_server:
        return plugin_config.jx3_default_server
    return None


# ===== 奇遇 =====
cmd_adventure = on_command("奇遇", rule=group_filter(), priority=5, block=True)


@cmd_adventure.handle()
async def handle_adventure(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_adventure.finish("请输入角色名，如：奇遇 赤瞳竹")

    server = await _get_server_for_role(event, args)
    if not server:
        await cmd_adventure.finish("请先绑定服务器")

    try:
        data = await api_client.event_records(server=server, name=name)
    except JX3APIError as e:
        await cmd_adventure.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("adventure.html", title=f"🎯 奇遇 · {name}", data=data, server=server)
    await cmd_adventure.finish(MessageSegment.image(img))


# ===== 未做奇遇 =====
cmd_unfinished = on_command("未做奇遇", rule=group_filter(), priority=5, block=True)


@cmd_unfinished.handle()
async def handle_unfinished(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_unfinished.finish("请输入角色名，如：未做奇遇 赤瞳竹")

    server = await _get_server_for_role(event, args)
    if not server:
        await cmd_unfinished.finish("请先绑定服务器")

    try:
        data = await api_client.event_unfinished(server=server, name=name)
    except JX3APIError as e:
        await cmd_unfinished.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"❓ 未做奇遇 · {name}", data=data)
    await cmd_unfinished.finish(MessageSegment.image(img))


# ===== 近期奇遇 =====
cmd_recent_adv = on_command("近期奇遇", rule=group_filter(), priority=5, block=True)


@cmd_recent_adv.handle()
async def handle_recent_adv(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_recent_adv.finish("请先绑定服务器或输入服务器名")

    try:
        data = await api_client.event_recent(server=server)
    except JX3APIError as e:
        await cmd_recent_adv.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"🕐 近期奇遇 · {server}", data=data)
    await cmd_recent_adv.finish(MessageSegment.image(img))


# ===== 奇遇统计 =====
cmd_adv_stats = on_command("奇遇统计", rule=group_filter(), priority=5, block=True)


@cmd_adv_stats.handle()
async def handle_adv_stats(event: GroupMessageEvent, args: Message = CommandArg()):
    text = args.extract_plain_text().strip()

    server = await _get_server_for_role(event, args)
    if not server:
        await cmd_adv_stats.finish("请先绑定服务器")

    try:
        data = await api_client.event_statistics(server=server, name=text)
    except JX3APIError as e:
        await cmd_adv_stats.finish(f"❌ 查询失败：{e.msg}")

    title = f"📊 奇遇统计" + (f" · {text}" if text else "")
    img = await renderer.render("table.html", title=title, data=data)
    await cmd_adv_stats.finish(MessageSegment.image(img))


# ===== 奇遇汇总 =====
cmd_adv_collect = on_command("奇遇汇总", rule=group_filter(), priority=5, block=True)


@cmd_adv_collect.handle()
async def handle_adv_collect(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_adv_collect.finish("请先绑定服务器")

    try:
        data = await api_client.event_collect(server=server)
    except JX3APIError as e:
        await cmd_adv_collect.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"📋 奇遇汇总 · {server}", data=data)
    await cmd_adv_collect.finish(MessageSegment.image(img))

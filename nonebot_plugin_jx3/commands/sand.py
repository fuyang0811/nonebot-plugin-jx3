"""commands/sand.py — 沙盘/阵营事件/诛恶指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter, get_server
from ..api_client import api_client, JX3APIError
from ..render import renderer


# ===== 沙盘 =====
cmd_sand = on_command("沙盘", rule=group_filter(), priority=5, block=True)


@cmd_sand.handle()
async def handle_sand(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_sand.finish("请先绑定服务器或输入服务器名，如：沙盘 绝代天骄")

    try:
        data = await api_client.sand_records(server=server)
    except JX3APIError as e:
        await cmd_sand.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("sand.html", title=f"🗺️ 沙盘 · {server}", data=data, server=server)
    await cmd_sand.finish(MessageSegment.image(img))


# ===== 阵营事件 =====
cmd_fenxian = on_command("阵营事件", rule=group_filter(), priority=5, block=True)


@cmd_fenxian.handle()
async def handle_fenxian(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_fenxian.finish("请先绑定服务器")

    try:
        data = await api_client.fenxian_records(server=server)
    except JX3APIError as e:
        await cmd_fenxian.finish(f"❌ 查询失败：{e.msg}")

    import datetime
    for item in data:
        if "seize_time" in item:
            ts = item["seize_time"]
            item["time_str"] = datetime.datetime.fromtimestamp(int(ts)).strftime('%m-%d %H:%M')

    img = await renderer.render(
        "table.html", 
        title=f"⚔️ 阵营事件", 
        data=data,
        columns=["camp_name", "fenxian_name", "role_name", "time_str"],
        headers=["阵营", "服务器", "角色名", "占领时间"]
    )
    await cmd_fenxian.finish(MessageSegment.image(img))


# ===== 诛恶 =====
cmd_smite = on_command("诛恶", rule=group_filter(), priority=5, block=True)


@cmd_smite.handle()
async def handle_smite(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_smite.finish("请先绑定服务器")

    try:
        data = await api_client.smite_records(server=server)
    except JX3APIError as e:
        await cmd_smite.finish(f"❌ 查询失败：{e.msg}")

    import datetime
    for item in data:
        if "time" in item:
            ts = item["time"]
            item["time_str"] = datetime.datetime.fromtimestamp(int(ts)).strftime('%m-%d %H:%M')

    img = await renderer.render(
        "table.html", 
        title=f"😈 诛恶事件 · {server}", 
        data=data,
        columns=["map_name", "time_str"],
        headers=["刷新地图", "刷新时间"]
    )
    await cmd_smite.finish(MessageSegment.image(img))

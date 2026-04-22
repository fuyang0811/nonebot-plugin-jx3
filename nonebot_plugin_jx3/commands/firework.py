"""commands/firework.py — 烟花/拍卖指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter, get_server
from ..api_client import api_client, JX3APIError
from ..render import renderer
from ..database import db


# ===== 烟花 =====
cmd_firework = on_command("烟花", rule=group_filter(), priority=5, block=True)


@cmd_firework.handle()
async def handle_firework(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_firework.finish("请输入角色名，如：烟花 赤瞳竹")

    server = None
    if hasattr(event, "group_id"):
        server = await db.get_server(event.group_id)
    if not server:
        from ..config import plugin_config
        server = plugin_config.jx3_default_server
    if not server:
        await cmd_firework.finish("请先绑定服务器")

    try:
        data = await api_client.show_records(server=server, name=name)
    except JX3APIError as e:
        await cmd_firework.finish(f"❌ 查询失败：{e.msg}")

    import datetime
    for item in data:
        if "time" in item:
            ts = item["time"]
            item["time_str"] = datetime.datetime.fromtimestamp(int(ts)).strftime('%m-%d %H:%M')

    img = await renderer.render(
        "table.html", 
        title=f"🎆 烟花记录 · {name}", 
        data=data,
        columns=["map_name", "sender", "receiver", "firework", "time_str"],
        headers=["地图", "赠送人", "接收人", "烟花名称", "赠送时间"]
    )
    await cmd_firework.finish(MessageSegment.image(img))


# ===== 拍卖 =====
cmd_auction = on_command("拍卖", rule=group_filter(), priority=5, block=True)


@cmd_auction.handle()
async def handle_auction(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_auction.finish("请先绑定服务器")

    try:
        data = await api_client.auction_records(server=server)
    except JX3APIError as e:
        await cmd_auction.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"🏛️ 阵营拍卖 · {server}", data=data)
    await cmd_auction.finish(MessageSegment.image(img))

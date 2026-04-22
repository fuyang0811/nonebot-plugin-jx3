"""commands/server.py — 开服/搜服指令"""
import datetime
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter, get_server
from ..api_client import api_client, JX3APIError
from ..render import renderer


# ===== 开服 =====
cmd_kaifu = on_command("开服", rule=group_filter(), priority=5, block=True)


@cmd_kaifu.handle()
async def handle_kaifu(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_kaifu.finish("请先绑定服务器或输入服务器名，如：开服 绝代天骄")

    try:
        data = await api_client.status_check(server=server)
    except JX3APIError as e:
        await cmd_kaifu.finish(f"❌ 查询失败：{e.msg}")

    status_map = {1: "🟢 良好", 0: "🔴 维护", 2: "🟠 繁忙", 3: "🔥 爆满"}
    fmt = {
        "大区": data.get("zone", ""),
        "服务器": data.get("server", server),
        "状态": status_map.get(data.get("status", 0), str(data.get("status", 0))),
        "上次开服": datetime.datetime.fromtimestamp(data["lasttime"]).strftime("%Y-%m-%d %H:%M:%S") if data.get("lasttime") else "未知",
        "上次维护": datetime.datetime.fromtimestamp(data["shuttime"]).strftime("%Y-%m-%d %H:%M:%S") if data.get("shuttime") else "未知",
    }
    img = await renderer.render("card.html", title=f"🖥️ 开服状态 · {server}", data=fmt)
    await cmd_kaifu.finish(MessageSegment.image(img))


# ===== 搜服 =====
cmd_search_server = on_command("搜服", rule=group_filter(), priority=5, block=True)


@cmd_search_server.handle()
async def handle_search_server(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_search_server.finish("请输入搜索关键字，如：搜服 长安")

    try:
        data = await api_client.master_search(name=name)
    except JX3APIError as e:
        await cmd_search_server.finish(f"❌ 查询失败：{e.msg}")

    if isinstance(data, list):
        d = data[0] if len(data) == 1 else None
    else:
        d = data if isinstance(data, dict) else None

    if d:
        aliases = d.get("alias", [])
        slaves = d.get("slave", [])
        fmt = {
            "主名称": d.get("name", ""),
            "大区": d.get("zone", ""),
            "中心节点": d.get("center", ""),
            "别名": "、".join(aliases[:5]) + ("..." if len(aliases) > 5 else ""),
            "合服记录": "、".join(slaves[:5]) + ("..." if len(slaves) > 5 else ""),
        }
        img = await renderer.render("card.html", title=f"🔍 区服搜索 · {name}", data=fmt)
        await cmd_search_server.finish(MessageSegment.image(img))
    else:
        results = "\n".join(f"  {d.get('zone','')} - {d.get('server','')}" for d in data)
        await cmd_search_server.finish(f"🔍 搜索结果：\n{results}")

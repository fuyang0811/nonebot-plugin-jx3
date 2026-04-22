"""commands/daily.py — 日常/预测/月历/行侠指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter, get_server
from ..api_client import api_client, JX3APIError
from ..render import renderer


# ===== 日常 =====
cmd_daily = on_command("日常", rule=group_filter(), priority=5, block=True)


@cmd_daily.handle()
async def handle_daily(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_daily.finish("请先绑定服务器或输入服务器名，如：日常 绝代天骄")

    try:
        data = await api_client.active_calendar(server=server, num=0)
    except JX3APIError as e:
        await cmd_daily.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("calendar.html", data=data)
    await cmd_daily.finish(MessageSegment.image(img))


# ===== 预测 =====
cmd_predict = on_command("预测", rule=group_filter(), priority=5, block=True)


@cmd_predict.handle()
async def handle_predict(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_predict.finish("请先绑定服务器或输入服务器名")

    try:
        data = await api_client.active_calendar(server=server, num=1)
    except JX3APIError as e:
        await cmd_predict.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("calendar.html", data=data)
    await cmd_predict.finish(MessageSegment.image(img))


# ===== 月历 =====
cmd_monthly = on_command("月历", rule=group_filter(), priority=5, block=True)


@cmd_monthly.handle()
async def handle_monthly(event: GroupMessageEvent, args: Message = CommandArg()):
    try:
        raw = await api_client.active_list_calendar()
    except JX3APIError as e:
        await cmd_monthly.finish(f"❌ 查询失败：{e.msg}")

    raw_list = raw.get("data", []) if isinstance(raw, dict) else raw
    data = [
        {
            "date": f"{item.get('month', '')}-{item.get('day', '')}",
            "week": item.get("week", ""),
            "war": item.get("war", ""),
            "battle": item.get("battle", ""),
            "orecar": item.get("orecar", ""),
        }
        for item in raw_list[:15]
    ]

    img = await renderer.render(
        "table.html", title="📅 活动月历", data=data,
        columns=["date", "week", "war", "battle", "orecar"],
        headers=["日期", "星期", "大战", "战场", "矿车"]
    )
    await cmd_monthly.finish(MessageSegment.image(img))


# ===== 行侠 =====
cmd_celebs = on_command("行侠", rule=group_filter(), priority=5, block=True)


@cmd_celebs.handle()
async def handle_celebs(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()

    try:
        data = await api_client.active_celebs(name=name)
    except JX3APIError as e:
        await cmd_celebs.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title="🏃 行侠仗义", data=data)
    await cmd_celebs.finish(MessageSegment.image(img))

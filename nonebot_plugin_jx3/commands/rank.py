"""commands/rank.py — 榜单/试炼排行/掉落统计指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter, get_server
from ..api_client import api_client, JX3APIError
from ..render import renderer


# ===== 榜单 =====
cmd_rank = on_command("榜单", rule=group_filter(), priority=5, block=True)


@cmd_rank.handle()
async def handle_rank(event: GroupMessageEvent, args: Message = CommandArg()):
    text = args.extract_plain_text().strip()
    if not text:
        await cmd_rank.finish("请输入榜单类型，如：榜单 个人")

    server = await get_server(event, args)
    if not server:
        await cmd_rank.finish("请先绑定服务器")

    try:
        data = await api_client.rank_statistical(server=server, type=text)
    except JX3APIError as e:
        await cmd_rank.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"🏆 {text}榜单", data=data)
    await cmd_rank.finish(MessageSegment.image(img))


# ===== 试炼排行 =====
cmd_trials = on_command("试炼排行", rule=group_filter(), priority=5, block=True)


@cmd_trials.handle()
async def handle_trials(event: GroupMessageEvent, args: Message = CommandArg()):
    text = args.extract_plain_text().strip()

    server = await get_server(event, args)
    if not server:
        await cmd_trials.finish("请先绑定服务器")

    school = text if text else ""

    try:
        data = await api_client.rank_trials(server=server, school=school)
    except JX3APIError as e:
        await cmd_trials.finish(f"❌ 查询失败：{e.msg}")

    # 剥离外层包装
    if isinstance(data, dict):
        data = data.get("data", [])

    title = f"🗡️ 试炼排行" + (f" · {school}" if school else "")
    img = await renderer.render(
        "table.html",
        title=title,
        data=data,
        columns=["role_name", "max_level", "total_score", "equip_score"],
        headers=["角色名", "最高层数", "试炼分数", "装备分数"]
    )
    await cmd_trials.finish(MessageSegment.image(img))


# ===== 掉落 =====
cmd_reward = on_command("掉落", rule=group_filter(), priority=5, block=True)


@cmd_reward.handle()
async def handle_reward(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_reward.finish("请输入副本名称，如：掉落 敖龙岛")

    server = await get_server(event, args)
    if not server:
        await cmd_reward.finish("请先绑定服务器")

    try:
        data = await api_client.reward_statistics(server=server, name=name)
    except JX3APIError as e:
        await cmd_reward.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"🎁 掉落统计 · {name}", data=data)
    await cmd_reward.finish(MessageSegment.image(img))

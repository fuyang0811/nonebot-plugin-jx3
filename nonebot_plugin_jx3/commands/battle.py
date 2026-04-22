"""commands/battle.py — 帮战/解密/统战/关隘/百战/扶摇指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter, get_server
from ..api_client import api_client, JX3APIError
from ..render import renderer


# ===== 帮战 =====
cmd_battle = on_command("帮战", rule=group_filter(), priority=5, block=True)


@cmd_battle.handle()
async def handle_battle(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_battle.finish("请先绑定服务器")

    try:
        data = await api_client.battle_records(server=server)
    except JX3APIError as e:
        await cmd_battle.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"⚔️ 帮战记录 · {server}", data=data)
    await cmd_battle.finish(MessageSegment.image(img))


# ===== 解密 =====
cmd_mech = on_command("解密", rule=group_filter(), priority=5, block=True)


@cmd_mech.handle()
async def handle_mech(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_mech.finish("请输入副本名称，如：解密 敖龙岛")

    try:
        data = await api_client.mech_calculator(name=name)
    except JX3APIError as e:
        await cmd_mech.finish(f"❌ 查询失败：{e.msg}")

    if isinstance(data, dict):
        for k in ["curr", "next"]:
            if k in data and isinstance(data[k], dict):
                data[k] = f"{data[k].get('node', '')} - {data[k].get('data', '')}"

    img = await renderer.render("card.html", title=f"🔐 解密 · {name}", data=data)
    await cmd_mech.finish(MessageSegment.image(img))


# ===== 统战 =====
cmd_duowan = on_command("统战", rule=group_filter(), priority=5, block=True)


@cmd_duowan.handle()
async def handle_duowan(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_duowan.finish("请先绑定服务器")

    try:
        data = await api_client.duowan_statistics(server=server)
    except JX3APIError as e:
        await cmd_duowan.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("card.html", title=f"📊 统战歪歪 · {server}", data=data)
    await cmd_duowan.finish(MessageSegment.image(img))


# ===== 关隘 =====
cmd_mine = on_command("关隘", rule=group_filter(), priority=5, block=True)


@cmd_mine.handle()
async def handle_mine(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)

    try:
        data = await api_client.mine_cart(server=server or "")
    except JX3APIError as e:
        await cmd_mine.finish(f"❌ 查询失败：{e.msg}")

    # 数据扁平化处理
    formatted_data = []
    server_data = []
    if isinstance(data, list):
        for s_block in data:
            if isinstance(s_block, dict) and s_block.get("server") == server:
                server_data = s_block.get("data", [])
                break
    elif isinstance(data, dict):
        server_data = data.get(server, [])

    import datetime
    for item in server_data:
        if "start_time" in item:
            ts = item["start_time"]
            item["time_str"] = datetime.datetime.fromtimestamp(int(ts)).strftime('%m-%d %H:%M')
    formatted_data = server_data

    img = await renderer.render(
        "table.html", 
        title=f"👹 关隘首领 · {server}", 
        data=formatted_data,
        columns=["camp_name", "castle", "leader", "str_status", "time_str"],
        headers=["阵营", "关隘", "首领", "当前状态", "更新时间"]
    )
    await cmd_mine.finish(MessageSegment.image(img))


# ===== 百战 =====
cmd_monster = on_command("百战", rule=group_filter(), priority=5, block=True)


@cmd_monster.handle()
async def handle_monster(event: GroupMessageEvent, args: Message = CommandArg()):
    try:
        data = await api_client.active_monster()
    except JX3APIError as e:
        await cmd_monster.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("card.html", title="⚔️ 百战首领", data=data)
    await cmd_monster.finish(MessageSegment.image(img))


# ===== 扶摇 =====
cmd_fuyao = on_command("扶摇", rule=group_filter(), priority=5, block=True)


@cmd_fuyao.handle()
async def handle_fuyao(event: GroupMessageEvent, args: Message = CommandArg()):
    try:
        data = await api_client.active_next_event()
    except JX3APIError as e:
        await cmd_fuyao.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("card.html", title="☁️ 扶摇预测", data=data)
    await cmd_fuyao.finish(MessageSegment.image(img))

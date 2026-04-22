"""commands/school.py — 小药/技改/阵眼/奇穴/技能/资历指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter, get_server
from ..api_client import api_client, JX3APIError
from ..render import renderer


# ===== 小药 =====
cmd_foods = on_command("小药", rule=group_filter(), priority=5, block=True)


@cmd_foods.handle()
async def handle_foods(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_foods.finish("请输入心法名称，如：小药 花间游")

    try:
        data = await api_client.school_foods(name=name)
    except JX3APIError as e:
        await cmd_foods.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render(
        "table.html", 
        title=f"💊 小药推荐 · {name}", 
        data=data,
        columns=["class", "name", "boost"],
        headers=["类型", "物品名称", "增益效果"]
    )
    await cmd_foods.finish(MessageSegment.image(img))


# ===== 技改 =====
cmd_rework = on_command("技改", rule=group_filter(), priority=5, block=True)


@cmd_rework.handle()
async def handle_rework(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_rework.finish("请输入心法名称，如：技改 花间游")

    try:
        data = await api_client.skill_rework(name=name)
    except JX3APIError as e:
        await cmd_rework.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"🔧 技改记录 · {name}", data=data)
    await cmd_rework.finish(MessageSegment.image(img))


# ===== 阵眼 =====
cmd_matrix = on_command("阵眼", rule=group_filter(), priority=5, block=True)


@cmd_matrix.handle()
async def handle_matrix(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_matrix.finish("请输入心法名称，如：阵眼 花间游")

    try:
        data = await api_client.school_matrix(name=name)
    except JX3APIError as e:
        await cmd_matrix.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("matrix.html", title=f"👁️ 阵眼 · {name}", data=data)
    await cmd_matrix.finish(MessageSegment.image(img))


# ===== 奇穴 =====
cmd_talent = on_command("奇穴", rule=group_filter(), priority=5, block=True)


@cmd_talent.handle()
async def handle_talent(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_talent.finish("请输入心法名称，如：奇穴 花间游")

    try:
        data = await api_client.school_talent(name=name)
    except JX3APIError as e:
        await cmd_talent.finish(f"❌ 查询失败：{e.msg}")

    # ===== 扁平化深层奇穴嵌套结构 =====
    formatted_list = []
    for tier in data:
        level_num = tier.get("level", "")
        talents_arr = tier.get("data", [])
        talents_str = "、".join([x.get("name", "") for x in talents_arr])
        formatted_list.append({
            "level": f"第{level_num}重",
            "talents": talents_str
        })
    # ==================================

    img = await renderer.render(
        "table.html", 
        title=f"⭐ 奇穴 · {name}", 
        data=formatted_list,
        columns=["level", "talents"],
        headers=["重数", "奇穴选择"]
    )
    await cmd_talent.finish(MessageSegment.image(img))


# ===== 技能 =====
cmd_skills = on_command("技能", rule=group_filter(), priority=5, block=True)


@cmd_skills.handle()
async def handle_skills(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_skills.finish("请输入心法名称，如：技能 花间游")

    try:
        data = await api_client.school_skills(name=name)
    except JX3APIError as e:
        await cmd_skills.finish(f"❌ 查询失败：{e.msg}")
        
    # ===== 解析深层多维技能封装为扁平结构 =====
    formatted_list = []
    if isinstance(data, list):
        for item in data:
            category = item.get("class", "")
            skill_list = item.get("data", [])
            for skill in skill_list:
                formatted_list.append({
                    "category": category,
                    "name": skill.get("name", ""),
                    "interval": skill.get("interval", ""),
                    "simpleDesc": skill.get("simpleDesc", "")
                })
    # ==========================================

    img = await renderer.render(
        "table.html", 
        title=f"⚡ 技能 · {name}", 
        data=formatted_list,
        columns=["category", "name", "interval", "simpleDesc"],
        headers=["武学分类", "技能名称", "调息状态", "核心描述"]
    )
    await cmd_skills.finish(MessageSegment.image(img))


# ===== 资历 =====
cmd_seniority = on_command("资历", rule=group_filter(), priority=5, block=True)


@cmd_seniority.handle()
async def handle_seniority(event: GroupMessageEvent, args: Message = CommandArg()):
    text = args.extract_plain_text().strip()

    server = await get_server(event, args)
    if not server:
        await cmd_seniority.finish("请先绑定服务器或输入服务器名")

    # 解析可选的心法参数
    parts = text.split(maxsplit=1)
    school = parts[1] if len(parts) > 1 else ""

    try:
        data = await api_client.school_seniority(server=server, school=school)
    except JX3APIError as e:
        await cmd_seniority.finish(f"❌ 查询失败：{e.msg}")

    title = f"📊 资历排行" + (f" · {school}" if school else "")
    img = await renderer.render("table.html", title=title, data=data)
    await cmd_seniority.finish(MessageSegment.image(img))

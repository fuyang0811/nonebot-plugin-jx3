"""commands/recruit.py — 招募/师徒指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter, get_server
from ..api_client import api_client, JX3APIError
from ..render import renderer


# ===== 招募 =====
cmd_recruit = on_command("招募", rule=group_filter(), priority=5, block=True)


@cmd_recruit.handle()
async def handle_recruit(event: GroupMessageEvent, args: Message = CommandArg()):
    text = args.extract_plain_text().strip()

    server = await get_server(event, args)
    if not server:
        # 如果文本就是关键字，尝试从群绑定拿服务器
        from ..database import db
        if hasattr(event, "group_id"):
            server = await db.get_server(event.group_id)
        if not server:
            await cmd_recruit.finish("请先绑定服务器或输入服务器名")
        keyword = text
    else:
        keyword = ""

    try:
        data = await api_client.recruit_search(server=server, keyword=keyword)
    except JX3APIError as e:
        await cmd_recruit.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("recruit.html", title=f"📢 招募 · {server}", data=data)
    await cmd_recruit.finish(MessageSegment.image(img))


# ===== 师徒 =====
cmd_mentor = on_command("师徒", rule=group_filter(), priority=5, block=True)


@cmd_mentor.handle()
async def handle_mentor(event: GroupMessageEvent, args: Message = CommandArg()):
    text = args.extract_plain_text().strip()

    server = await get_server(event, args)
    if not server:
        from ..database import db
        if hasattr(event, "group_id"):
            server = await db.get_server(event.group_id)
        if not server:
            await cmd_mentor.finish("请先绑定服务器或输入服务器名")
        keyword = text
    else:
        keyword = ""

    try:
        data = await api_client.mentor_search(server=server, keyword=keyword)
    except JX3APIError as e:
        await cmd_mentor.finish(f"❌ 查询失败：{e.msg}")

    # 剥离外层包装，提取师徒列表
    if isinstance(data, dict):
        data = data.get("data", [])

    img = await renderer.render(
        "table.html",
        title=f"🎓 师徒招募 · {server}",
        data=data,
        columns=["campName", "bodyName", "forceName", "roleName", "comment"],
        headers=["阵营", "体型", "门派", "角色名", "招募宣言"]
    )
    await cmd_mentor.finish(MessageSegment.image(img))

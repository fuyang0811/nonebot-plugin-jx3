"""commands/home.py — 鲜花/装饰/图谱指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter, get_server
from ..api_client import api_client, JX3APIError
from ..render import renderer


# ===== 鲜花 =====
cmd_flower = on_command("鲜花", rule=group_filter(), priority=5, block=True)


@cmd_flower.handle()
async def handle_flower(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_flower.finish("请先绑定服务器或输入服务器名，如：鲜花 绝代天骄")

    try:
        data = await api_client.home_flower(server=server)
    except JX3APIError as e:
        await cmd_flower.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("flower.html", title=f"🌸 家园鲜花 · {server}", data=data)
    await cmd_flower.finish(MessageSegment.image(img))


# ===== 装饰 =====
cmd_furniture = on_command("装饰", rule=group_filter(), priority=5, block=True)


@cmd_furniture.handle()
async def handle_furniture(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_furniture.finish("请输入装饰名称，如：装饰 红梅")

    try:
        data = await api_client.home_furniture(name=name)
    except JX3APIError as e:
        await cmd_furniture.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("card.html", title=f"🏠 装饰 · {name}", data=data)
    await cmd_furniture.finish(MessageSegment.image(img))


# ===== 图谱 =====
cmd_travel = on_command("图谱", rule=group_filter(), priority=5, block=True)


@cmd_travel.handle()
async def handle_travel(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_travel.finish("请输入器物名称，如：图谱 生炉")

    try:
        data = await api_client.home_travel(name=name)
    except JX3APIError as e:
        await cmd_travel.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("card.html", title=f"📜 图谱 · {name}", data=data)
    await cmd_travel.finish(MessageSegment.image(img))

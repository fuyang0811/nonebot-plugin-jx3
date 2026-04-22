"""commands/role.py — 角色信息/名片/百战指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter
from ..api_client import api_client, JX3APIError
from ..render import renderer
from ..database import db


async def _get_server(event):
    """获取群绑定服务器"""
    if hasattr(event, "group_id"):
        server = await db.get_server(event.group_id)
        if server:
            return server
    from ..config import plugin_config
    return plugin_config.jx3_default_server or None


# ===== 角色 =====
cmd_role = on_command("角色", rule=group_filter(), priority=5, block=True)


@cmd_role.handle()
async def handle_role(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_role.finish("请输入角色名，如：角色 赤瞳竹")

    server = await _get_server(event)
    if not server:
        await cmd_role.finish("请先绑定服务器")

    try:
        data = await api_client.role_detail(server=server, name=name)
    except JX3APIError as e:
        await cmd_role.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("role.html", title=f"📋 角色 · {name}", data=data, server=server)
    await cmd_role.finish(MessageSegment.image(img))


# ===== 名片 =====
cmd_card = on_command("名片", rule=group_filter(), priority=5, block=True)


@cmd_card.handle()
async def handle_card(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_card.finish("请输入角色名，如：名片 赤瞳竹")

    server = await _get_server(event)
    if not server:
        await cmd_card.finish("请先绑定服务器")

    try:
        data = await api_client.card_record(server=server, name=name)
    except JX3APIError as e:
        await cmd_card.finish(f"❌ 查询失败：{e.msg}")

    # 名片通常返回图片URL
    url = data.get("url", data.get("image", ""))
    if url:
        await cmd_card.finish(MessageSegment.image(url))
    else:
        img = await renderer.render("card.html", title=f"🃏 名片 · {name}", data=data)
        await cmd_card.finish(MessageSegment.image(img))


# ===== 所有名片 =====
cmd_cards = on_command("所有名片", rule=group_filter(), priority=5, block=True)


@cmd_cards.handle()
async def handle_cards(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_cards.finish("请输入角色名，如：所有名片 赤瞳竹")

    server = await _get_server(event)
    if not server:
        await cmd_cards.finish("请先绑定服务器")

    try:
        data = await api_client.card_records(server=server, name=name)
    except JX3APIError as e:
        await cmd_cards.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"🃏 所有名片 · {name}", data=data)
    await cmd_cards.finish(MessageSegment.image(img))


# ===== 缓存名片 =====
cmd_card_cached = on_command("缓存名片", rule=group_filter(), priority=5, block=True)


@cmd_card_cached.handle()
async def handle_card_cached(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_card_cached.finish("请输入角色名，如：缓存名片 赤瞳竹")

    server = await _get_server(event)
    if not server:
        await cmd_card_cached.finish("请先绑定服务器")

    try:
        data = await api_client.card_cached(server=server, name=name)
    except JX3APIError as e:
        await cmd_card_cached.finish(f"❌ 查询失败：{e.msg}")

    url = data.get("url", data.get("image", ""))
    if url:
        await cmd_card_cached.finish(MessageSegment.image(url))
    else:
        img = await renderer.render("card.html", title=f"🃏 缓存名片 · {name}", data=data)
        await cmd_card_cached.finish(MessageSegment.image(img))


# ===== 角色百战 =====
cmd_role_monster = on_command("角色百战", rule=group_filter(), priority=5, block=True)


@cmd_role_monster.handle()
async def handle_role_monster(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_role_monster.finish("请输入角色名，如：角色百战 赤瞳竹")

    server = await _get_server(event)
    if not server:
        await cmd_role_monster.finish("请先绑定服务器")

    try:
        data = await api_client.role_monster(server=server, name=name)
    except JX3APIError as e:
        await cmd_role_monster.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"⚔️ 百战 · {name}", data=data)
    await cmd_role_monster.finish(MessageSegment.image(img))

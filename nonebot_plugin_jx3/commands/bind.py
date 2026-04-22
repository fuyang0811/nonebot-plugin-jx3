"""commands/bind.py — 绑定服务器指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.params import CommandArg

from ..utils import group_filter
from ..database import db


# ===== 绑定服务器 =====
cmd_bind = on_command(
    "绑定", rule=group_filter(), priority=5, block=True,
    permission=GROUP_OWNER | GROUP_ADMIN
)


@cmd_bind.handle()
async def handle_bind(event: GroupMessageEvent, args: Message = CommandArg()):
    server = args.extract_plain_text().strip()
    if not server:
        await cmd_bind.finish("请输入服务器名称，如：绑定 绝代天骄")

    await db.set_server(event.group_id, server)
    await cmd_bind.finish(f"✅ 已将本群绑定至【{server}】服务器")

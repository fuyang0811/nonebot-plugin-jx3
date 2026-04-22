"""工具函数：群过滤、服务器解析、时间格式化"""
import datetime
from typing import Optional

from nonebot.rule import Rule
from nonebot.adapters import Message


def group_filter() -> Rule:
    """群号白名单过滤规则。
    - jx3_enabled_groups 为空 → 所有群可用
    - jx3_enabled_groups 非空 → 仅列表中的群可用
    - 私聊不限制
    """
    async def _check(event) -> bool:
        from .config import plugin_config
        if not hasattr(event, "group_id"):
            return True
        if not plugin_config.jx3_enabled_groups:
            return True
        return event.group_id in plugin_config.jx3_enabled_groups
    return Rule(_check)


async def get_server(event, args: Message) -> Optional[str]:
    """解析服务器名。优先级：用户输入 > 群绑定 > 默认配置"""
    from .config import plugin_config
    from .database import db

    text = args.extract_plain_text().strip()
    if text:
        return text
    if hasattr(event, "group_id"):
        server = await db.get_server(event.group_id)
        if server:
            return server
    if plugin_config.jx3_default_server:
        return plugin_config.jx3_default_server
    return None


async def get_server_with_arg(event, args: Message):
    """解析服务器名和附加参数。
    支持格式：
    - "服务器名 参数" → (服务器名, 参数)
    - "参数" → (群绑定服务器, 参数)
    - "" → (群绑定服务器, "")
    """
    from .config import plugin_config
    from .database import db

    text = args.extract_plain_text().strip()
    parts = text.split(maxsplit=1)

    if len(parts) >= 2:
        # 可能是 "服务器 角色名" 或 "角色名 其他"
        # 尝试第一个词作为服务器
        return parts[0], parts[1]
    elif len(parts) == 1:
        # 单个参数，可能是服务器名或角色名
        # 由调用方决定语义
        return None, parts[0]
    else:
        server = None
        if hasattr(event, "group_id"):
            server = await db.get_server(event.group_id)
        if not server and plugin_config.jx3_default_server:
            server = plugin_config.jx3_default_server
        return server, ""


def format_ts(timestamp: int) -> str:
    """Unix 时间戳 → HH:MM 格式"""
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.strftime("%H:%M")


def format_date(timestamp: int) -> str:
    """Unix 时间戳 → YYYY-MM-DD HH:MM 格式"""
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M")

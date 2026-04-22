"""commands/news.py — 新闻/公告指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter
from ..api_client import api_client, JX3APIError
from ..render import renderer


# ===== 新闻 =====
cmd_news = on_command("新闻", rule=group_filter(), priority=5, block=True)


@cmd_news.handle()
async def handle_news(event: GroupMessageEvent, args: Message = CommandArg()):
    try:
        data = await api_client.news_allnews(limit=10)
    except JX3APIError as e:
        await cmd_news.finish(f"❌ 查询失败：{e.msg}")

    msg_lines = ["📰 【最新新闻资讯】"]
    for idx, item in enumerate(data[:10], 1):
        news_type = item.get("type", "官方")
        title = item.get("title", "")
        date = item.get("date", "")
        url = item.get("url", "")
        msg_lines.append(f"{idx}. [{news_type}] {title} ({date})\n   🔗 {url}")
        
    await cmd_news.finish("\n".join(msg_lines))


# ===== 公告 =====
cmd_announce = on_command("公告", rule=group_filter(), priority=5, block=True)


@cmd_announce.handle()
async def handle_announce(event: GroupMessageEvent, args: Message = CommandArg()):
    try:
        data = await api_client.news_announce(limit=5)
    except JX3APIError as e:
        await cmd_announce.finish(f"❌ 查询失败：{e.msg}")

    msg_lines = ["📢 【最新维护公告】"]
    for idx, item in enumerate(data[:5], 1):
        news_type = item.get("type", "公告")
        title = item.get("title", "")
        date = item.get("date", "")
        url = item.get("url", "")
        msg_lines.append(f"{idx}. [{news_type}] {title} ({date})\n   🔗 {url}")
        
    await cmd_announce.finish("\n".join(msg_lines))

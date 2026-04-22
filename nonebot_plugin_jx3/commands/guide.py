"""commands/guide.py — 本地奇遇攻略 + 定时阵营提醒"""
import csv
import os

from nonebot import on_command, require, get_bot
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter
from ..database import db

# ===== 定时阵营提醒 =====
scheduler = require("nonebot_plugin_apscheduler").scheduler


async def _send_camp_reminder(message: str):
    """发送阵营活动提醒到所有订阅群"""
    try:
        bot = get_bot()
    except Exception:
        return

    for gid in await db.get_groups_by_subscribe("阵营活动提醒"):
        try:
            await bot.send_group_msg(group_id=gid, message=message)
        except Exception:
            pass


# 周二、周四 19:20 小攻防提醒
scheduler.add_job(
    _send_camp_reminder, "cron",
    day_of_week="1,3", hour=19, minute=20,
    args=["⚔️ 阵营小攻防将在 20:00 开始，请于 19:28 排队。"]
)

# 周六、周日 12:20 和 18:20 攻防提醒
scheduler.add_job(
    _send_camp_reminder, "cron",
    day_of_week="5,6", hour=18, minute=20,
    args=["⚔️ 阵营攻防将在 19:00 开始，请于 18:30 排队。"]
)

scheduler.add_job(
    _send_camp_reminder, "cron",
    day_of_week="5,6", hour=12, minute=20,
    args=["⚔️ 阵营攻防将在 13:00 开始，请于 12:30 排队。"]
)

# 周三、周五 19:30 世界BOSS提醒
scheduler.add_job(
    _send_camp_reminder, "cron",
    day_of_week="2,4", hour=19, minute=30,
    args=["👹 跨服·烂柯山 世界BOSS 将在 20:00（分线 20:05）进行。"]
)

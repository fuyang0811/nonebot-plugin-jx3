"""commands/exam.py — 科举答题指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter
from ..api_client import api_client, JX3APIError
from ..render import renderer


# ===== 科举 =====
cmd_exam = on_command("科举", rule=group_filter(), priority=5, block=True)


@cmd_exam.handle()
async def handle_exam(event: GroupMessageEvent, args: Message = CommandArg()):
    subject = args.extract_plain_text().strip()
    if not subject:
        await cmd_exam.finish("请输入题目关键字，如：科举 太白")

    try:
        data = await api_client.exam_search(subject=subject, limit=5)
    except JX3APIError as e:
        await cmd_exam.finish(f"❌ 查询失败：{e.msg}")

    if not data:
        await cmd_exam.finish("❌ 未找到相关题目")

    # 构建文本回复（科举答案简短，不需要图片）
    lines = []
    for i, item in enumerate(data[:5], 1):
        q = item.get("question", item.get("title", ""))
        a = item.get("answer", "")
        lines.append(f"{i}. {q}\n   ✅ {a}")

    await cmd_exam.finish("\n".join(lines))

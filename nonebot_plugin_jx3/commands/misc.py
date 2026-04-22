"""commands/misc.py — 骚话/舔狗/八卦/语音/骗子指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter
from ..api_client import api_client, JX3APIError


# ===== 骚话 =====
cmd_saohua = on_command("骚话", rule=group_filter(), priority=5, block=True)


@cmd_saohua.handle()
async def handle_saohua(event: GroupMessageEvent, args: Message = CommandArg()):
    try:
        data = await api_client.saohua_random()
    except JX3APIError as e:
        await cmd_saohua.finish(f"❌ 获取失败：{e.msg}")

    await cmd_saohua.finish(data.get("text", "暂无骚话"))


# ===== 舔狗 =====
cmd_tiangou = on_command("舔狗", rule=group_filter(), priority=5, block=True)


@cmd_tiangou.handle()
async def handle_tiangou(event: GroupMessageEvent, args: Message = CommandArg()):
    try:
        data = await api_client.saohua_content()
    except JX3APIError as e:
        await cmd_tiangou.finish(f"❌ 获取失败：{e.msg}")

    await cmd_tiangou.finish(data.get("text", "暂无日记"))


# ===== 八卦 =====
cmd_bagua = on_command("八卦", rule=group_filter(), priority=5, block=True)


@cmd_bagua.handle()
async def handle_bagua(event: GroupMessageEvent, args: Message = CommandArg()):
    tags = args.extract_plain_text().strip() or "818"
    try:
        data = await api_client.tieba_random(tags=tags)
    except JX3APIError as e:
        await cmd_bagua.finish(f"❌ 获取失败：{e.msg}")

    title = data.get("title", "")
    url = data.get("url", "")
    server = data.get("server", "")
    cls = data.get("class", "")

    msg = f"📢 {title}"
    if server and server != "-":
        msg += f"\n🌐 服务器：{server}"
    if cls:
        msg += f"\n📁 分类：{cls}"
    if url:
        msg += f"\n🔗 {url}"

    await cmd_bagua.finish(msg)





# ===== 骗子 =====
cmd_fraud = on_command("骗子", rule=group_filter(), priority=5, block=True)


@cmd_fraud.handle()
async def handle_fraud(event: GroupMessageEvent, args: Message = CommandArg()):
    qq = args.extract_plain_text().strip()
    if not qq:
        await cmd_fraud.finish("请输入 QQ 号，如：骗子 123456")

    try:
        uin = int(qq)
    except ValueError:
        await cmd_fraud.finish("❌ 请输入正确的 QQ 号")

    try:
        data = await api_client.fraud_detail(uin=uin)
    except JX3APIError as e:
        if e.code == 404:
            await cmd_fraud.finish(f"✅ QQ {uin} 未在骗子库中记录")
        await cmd_fraud.finish(f"❌ 查询失败：{e.msg}")

    # 有记录
    records = data if isinstance(data, list) else [data]
    lines = [f"⚠️ QQ {uin} 骗子记录："]
    for r in records:
        server = r.get("server", "")
        detail = r.get("detail", r.get("content", ""))
        lines.append(f"  🌐 {server}：{detail}")

    await cmd_fraud.finish("\n".join(lines))

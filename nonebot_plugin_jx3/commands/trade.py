"""commands/trade.py — 金价/黑市/物价/搜索/贴吧指令"""
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import group_filter, get_server
from ..api_client import api_client, JX3APIError
from ..render import renderer
from ..chart import generate_gold_trend_base64


# ===== 金价 =====
cmd_gold = on_command("金价", rule=group_filter(), priority=5, block=True)


@cmd_gold.handle()
async def handle_gold(event: GroupMessageEvent, args: Message = CommandArg()):
    server = await get_server(event, args)
    if not server:
        await cmd_gold.finish("请先绑定服务器或输入服务器名，如：金价 绝代天骄")

    try:
        data = await api_client.trade_demon(server=server)
    except JX3APIError as e:
        await cmd_gold.finish(f"❌ 查询失败：{e.msg}")

    # 调用内置 matplotlib 函数提取 30天的绘图与极值计算报告
    chart_b64, stats = generate_gold_trend_base64(data)
    
    # 获取最新的5天数据留给底部表格对照
    # 由于数据是从新到旧，直接取前五个即可，或是重新基于日期逆序（保险起见）
    sorted_data = sorted(data, key=lambda x: x.get('date', ''), reverse=True)
    recent_data = sorted_data[:5]

    img = await renderer.render(
        "gold_trend.html", 
        title=f"💰 金价走势(30天) · {server}", 
        chart_b64=chart_b64,
        stats=stats,
        recent_data=recent_data
    )
    await cmd_gold.finish(MessageSegment.image(img))


# ===== 黑市 =====
cmd_trade = on_command("黑市", rule=group_filter(), priority=5, block=True)


@cmd_trade.handle()
async def handle_trade(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_trade.finish("请输入物品名称，如：黑市 小橙武")

    try:
        data = await api_client.trade_records(name=name)
    except JX3APIError as e:
        await cmd_trade.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"🏪 黑市 · {name}", data=data)
    await cmd_trade.finish(MessageSegment.image(img))


# ===== 物价 =====
cmd_item_price = on_command("物价", rule=group_filter(), priority=5, block=True)


@cmd_item_price.handle()
async def handle_item_price(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_item_price.finish("请输入物品名称，如：物价 小橙武")

    try:
        data = await api_client.trade_item_records(name=name)
    except JX3APIError as e:
        await cmd_item_price.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"📈 物价 · {name}", data=data)
    await cmd_item_price.finish(MessageSegment.image(img))


# ===== 搜索物品 =====
cmd_search_item = on_command("搜索物品", rule=group_filter(), priority=5, block=True)


@cmd_search_item.handle()
async def handle_search_item(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_search_item.finish("请输入物品关键字，如：搜索物品 橙武")

    try:
        data = await api_client.trade_item_search(name=name)
    except JX3APIError as e:
        await cmd_search_item.finish(f"❌ 查询失败：{e.msg}")

    if not data:
        await cmd_search_item.finish("❌ 未找到相关物品")

    if isinstance(data, list):
        lines = [f"🔍 搜索结果（{len(data)} 条）："]
        for item in data[:20]:
            n = item.get("name", str(item))
            lines.append(f"  · {n}")
        await cmd_search_item.finish("\n".join(lines))
    else:
        await cmd_search_item.finish(f"🔍 搜索结果：{data}")


# ===== 贴吧物价 =====
cmd_tieba_price = on_command("贴吧物价", rule=group_filter(), priority=5, block=True)


@cmd_tieba_price.handle()
async def handle_tieba_price(event: GroupMessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await cmd_tieba_price.finish("请输入物品名称，如：贴吧物价 小橙武")

    try:
        data = await api_client.tieba_item_records(name=name)
    except JX3APIError as e:
        await cmd_tieba_price.finish(f"❌ 查询失败：{e.msg}")

    img = await renderer.render("table.html", title=f"📊 贴吧物价 · {name}", data=data)
    await cmd_tieba_price.finish(MessageSegment.image(img))

"""WebSocket 事件处理。
每个 handler 负责：
1. 从 detail 构建消息文本
2. 根据 server + 订阅名 查找目标群
3. 发送消息
"""
from typing import Callable, Dict

from nonebot import get_bot, logger

from ..database import db
from ..utils import format_ts


async def _send_to_groups(server: str, subscribe: str, message: str):
    """发送消息到所有订阅了指定事件且绑定了对应服务器的群。
    server 为空时发送给所有订阅群。
    """
    try:
        bot = get_bot()
    except Exception:
        return

    if server:
        bind_groups = set(await db.get_groups_by_server(server))
        sub_groups = set(await db.get_groups_by_subscribe(subscribe))
        target = bind_groups & sub_groups
    else:
        target = set(await db.get_groups_by_subscribe(subscribe))

    for gid in target:
        try:
            await bot.send_group_msg(group_id=gid, message=message)
        except Exception as e:
            logger.error(f"[JX3] 发送到群 {gid} 失败: {e}")


# ============================================================
# 事件处理函数
# ============================================================

async def handle_1001(action: int, detail: dict):
    """奇遇报时"""
    name = detail["name"]
    event = detail["event"]
    server = detail["server"]
    level = detail.get("level", 1)

    msg = f"🎉 恭喜玩家 {name} 触发奇遇 [{event}]"
    await _send_to_groups(server, "奇遇", msg)

    if level == 2:
        msg = f"🌟 恭喜玩家 {name} 触发绝世奇遇 [{event}]！"
        await _send_to_groups(server, "绝世奇遇", msg)


async def handle_1002(action: int, detail: dict):
    """刷马事件"""
    server = detail["server"]
    map_name = detail["map_name"]
    time = format_ts(detail["time"])
    msg = f"🐴 [{time}] 将有宝马良驹出现在 {map_name}"
    await _send_to_groups(server, "抓马", msg)


async def handle_1003(action: int, detail: dict):
    """抓马事件"""
    server = detail["server"]
    name = detail["name"]
    map_name = detail["map_name"]
    horse = detail["horse"]
    msg = f"🐴 恭喜玩家 {name} 在 {map_name} 抓获 [{horse}]"
    await _send_to_groups(server, "抓马", msg)


async def handle_1004(action: int, detail: dict):
    """扶摇开启"""
    server = detail["server"]
    time = format_ts(detail["time"])
    msg = f"☁️ [{time}] 扶摇九天已开启"
    await _send_to_groups(server, "扶摇", msg)


async def handle_1005(action: int, detail: dict):
    """扶摇点名（单人）"""
    server = detail["server"]
    name = detail.get("name", "")
    msg = f"☁️ 玩家 {name} 获得扶摇点名"
    await _send_to_groups(server, "扶摇", msg)


async def handle_1006(action: int, detail: dict):
    """扶摇点名（多人）"""
    server = detail["server"]
    names = detail.get("name", [])
    if isinstance(names, list):
        names_str = "、".join(f"【{n}】" for n in names)
    else:
        names_str = str(names)
    msg = f"☁️ 以下玩家获得扶摇点名：{names_str}"
    await _send_to_groups(server, "扶摇", msg)


async def handle_1007(action: int, detail: dict):
    """烟花报时"""
    server = detail["server"]
    name = detail.get("name", "")
    map_name = detail.get("map_name", "")
    sender = detail.get("sender", "")
    recipient = detail.get("recipient", "")
    msg = f"🎆 {sender} 在 {map_name} 对 {recipient} 放了烟花 [{name}]"
    await _send_to_groups(server, "烟花", msg)


async def handle_1008_1011(action: int, detail: dict):
    """的卢事件 (1008=刷新, 1009=捕获, 1010=竞拍, 1011=击毙)"""
    server = detail["server"]
    labels = {1008: "刷新", 1009: "捕获", 1010: "竞拍", 1011: "击毙"}
    label = labels.get(action, "事件")
    map_name = detail.get("map_name", "")
    name = detail.get("name", "")
    msg = f"🐎 的卢{label}！{name} {map_name}"
    await _send_to_groups(server, "的卢", msg)


async def handle_1012(action: int, detail: dict):
    """玄晶报时"""
    server = detail["server"]
    role_name = detail.get("role_name", detail.get("name", ""))
    map_name = detail.get("map_name", "")
    name = detail.get("name", "")
    msg = f"💎 恭喜玩家 {role_name} 在 {map_name} 获得 [{name}]"
    await _send_to_groups(server, "玄晶", msg)


async def handle_1013(action: int, detail: dict):
    """阵营拍卖"""
    server = detail["server"]
    msg = "🏛️ 阵营拍卖信息更新"
    await _send_to_groups(server, "阵营拍卖", msg)


async def handle_1014(action: int, detail: dict):
    """诛恶事件"""
    server = detail["server"]
    map_name = detail["map_name"]
    time = format_ts(detail["time"])
    msg = f"⚔️ [{time}] 诛恶事件触发！众侠士可前往【{map_name}】一探究竟"
    await _send_to_groups(server, "诛恶", msg)


async def handle_1015(action: int, detail: dict):
    """追魂点名"""
    server = detail["server"]
    name = detail.get("name", "")
    msg = f"👻 追魂点名：{name}"
    await _send_to_groups(server, "追魂", msg)


async def handle_1016_1017(action: int, detail: dict):
    """阵营祭天 (1016=开始, 1017=结束)"""
    server = detail["server"]
    camp = detail.get("camp_name", "")
    label = "开始" if action == 1016 else "结束"
    msg = f"🏮 {camp} 阵营祭天{label}"
    await _send_to_groups(server, "祭天", msg)


async def handle_1101(action: int, detail: dict):
    """领地宣战开始"""
    server = detail["server"]
    d = detail.get("declaring_tong_name", "")
    a = detail.get("accepting_tong_name", "")
    b = detail.get("battlefield_tong_name", "")
    msg = f"⚔️ 【{d}】向【{a}】发起领地宣战，战场：{b}"
    await _send_to_groups(server, "攻防实况", msg)


async def handle_1102(action: int, detail: dict):
    """领地宣战结束"""
    server = detail["server"]
    v = detail.get("victory_tong_name", "")
    s = detail.get("victory_score", "")
    msg = f"⚔️ 领地宣战结束，{v} 获胜，得分 {s}"
    await _send_to_groups(server, "攻防实况", msg)


async def handle_1103(action: int, detail: dict):
    """帮会宣战开始"""
    server = detail["server"]
    d = detail.get("declaring_tong_name", "")
    a = detail.get("accepting_tong_name", "")
    msg = f"⚔️ 【{d}】向【{a}】发起帮会宣战"
    await _send_to_groups(server, "攻防实况", msg)


async def handle_1104(action: int, detail: dict):
    """帮会宣战结束"""
    server = detail["server"]
    v = detail.get("victory_tong_name", "")
    msg = f"⚔️ 帮会宣战结束，{v} 获胜"
    await _send_to_groups(server, "攻防实况", msg)


async def handle_gongfang(action: int, detail: dict):
    """攻防实况通用处理 (1111~1122)"""
    server = detail["server"]

    castle = detail.get("castle_name", detail.get("castle", ""))
    camp = detail.get("camp_name", "")
    tong = detail.get("tong_name", "")

    if action == 1111:
        msg = f"🏰 {castle} 据点粮仓被 {camp} 洗劫"
    elif action == 1112:
        msg = f"🏰 {castle} 据点大旗被大将重置"
    elif action == 1113:
        map_name = detail.get("map_name", "")
        msg = f"🏰 {camp} 位于 {map_name} 的 {castle} 据点大旗被夺"
    elif action in (1114, 1115):
        tong_text = f"的 {tong} " if tong else ""
        msg = f"🏰 {camp} {tong_text}成功占领 {castle} 据点"
    elif action in (1116, 1117, 1118):
        tongs = tong if isinstance(tong, list) else [tong]
        msg = f"🏰 {camp} 贡献前列帮会：{'、'.join(str(t) for t in tongs)}"
    elif action == 1119:
        role = detail.get("role_name", "")
        item = detail.get("item_name", "")
        amount = detail.get("item_amount", "")
        msg = f"🏰 {camp} {role} 以 {amount} 拍得 [{item}]"
    elif action in (1120, 1121, 1122):
        tongs = tong if isinstance(tong, list) else [tong]
        amount = detail.get("split_amount", "")
        msg = f"🏰 {camp} 拍卖分红 {amount}：{'、'.join(str(t) for t in tongs)}"
    else:
        msg = f"🏰 攻防事件 {action}"

    await _send_to_groups(server, "攻防实况", msg)


async def handle_2001(action: int, detail: dict):
    """开服报时"""
    server = detail["server"]
    status = "开服" if detail["status"] == 1 else "维护"
    msg = f"🖥️ {server} 已{status}"
    await _send_to_groups(server, "开服", msg)


async def handle_2002(action: int, detail: dict):
    """新闻资讯"""
    title = detail.get("title", "")
    url = detail.get("url", "")
    type_ = detail.get("class", detail.get("type", ""))
    msg = f"📰 {type_}：{title}\n{url}"
    await _send_to_groups("", "新闻", msg)


async def handle_2003(action: int, detail: dict):
    """游戏更新"""
    old = detail.get("now_version", "")
    new = detail.get("new_version", "")
    size = detail.get("package_size", "")
    msg = f"🔄 游戏更新 {old} → {new}，大小：{size}"
    await _send_to_groups("", "更新", msg)


async def handle_2004(action: int, detail: dict):
    """八卦速报"""
    title = detail.get("title", "")
    url = detail.get("url", "")
    server = detail.get("server", "")
    if server == "-":
        server = ""
    msg = f"📢 {title}\n🔗 {url}"
    await _send_to_groups(server, "818", msg)


async def handle_2005(action: int, detail: dict):
    """关隘首领"""
    server = detail.get("server", "")
    msg = "👹 关隘首领事件"
    await _send_to_groups(server, "关隘", msg)


async def handle_2006(action: int, detail: dict):
    """云丛预告"""
    server = detail.get("server", "")
    msg = "☁️ 云丛预告"
    await _send_to_groups(server, "云丛", msg)


# ============================================================
# Handler 注册表
# ============================================================
HANDLER_MAP: Dict[int, Callable] = {
    1001: handle_1001,
    1002: handle_1002,
    1003: handle_1003,
    1004: handle_1004,
    1005: handle_1005,
    1006: handle_1006,
    1007: handle_1007,
    1008: handle_1008_1011,
    1009: handle_1008_1011,
    1010: handle_1008_1011,
    1011: handle_1008_1011,
    1012: handle_1012,
    1013: handle_1013,
    1014: handle_1014,
    1015: handle_1015,
    1016: handle_1016_1017,
    1017: handle_1016_1017,
    1101: handle_1101,
    1102: handle_1102,
    1103: handle_1103,
    1104: handle_1104,
    **{i: handle_gongfang for i in range(1111, 1123)},
    2001: handle_2001,
    2002: handle_2002,
    2003: handle_2003,
    2004: handle_2004,
    2005: handle_2005,
    2006: handle_2006,
}

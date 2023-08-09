import asyncio
import datetime

from aiohttp import ClientSession, ClientTimeout
from nonebot import require, get_bot

from .bind import get_bind_group
from .subscribe import get_subscribe_group

loop = False
from nonebot import get_driver
from .config import Config

plugin_config = Config.parse_obj(get_driver().config)
robot = plugin_config.jx3_bot_name
head = plugin_config.jx3_command_header
ticket = plugin_config.jx3_tuilan_ticket
token = plugin_config.jx3api_key
wss_token = plugin_config.jx3wss_token
scheduler = require("nonebot_plugin_apscheduler").scheduler
if wss_token == "":
    wssheaders = {}
else:
    wssheaders = {"token": wss_token}


async def get_group_ids(server: str, subscribe):
    if server is None or server == "":
        group_ids = await get_subscribe_group(subscribe)
    else:
        group_ids = list(set(await get_bind_group(server)) & set(await get_subscribe_group(subscribe)))

    print(group_ids)
    return group_ids


async def websocket_handler():
    global ws_connected, connected, loop
    while True:
        # config = get_driver().config.plugin_setting
        try:
            async with ClientSession(timeout=ClientTimeout(total=1)) as session:
                async with session.ws_connect("wss://socket.nicemoe.cn", headers=wssheaders,timeout=1) as ws:
                    ws_connected = ws
                    print("连接成功")
                    loop = True
                    while True:
                        msg = await ws.receive()
                        print(msg)
                        if msg.type == 1:  # Text message received
                            msg = msg.json()
                            # print(data)
                            action = msg["action"]
                            # print(action)
                            data = msg["data"]
                            if action == 2004:
                                asyncio.create_task(send_tieba(data))
                            elif action == 1009:
                                asyncio.create_task(send_zhue(data))
                            elif action == 1002:
                                asyncio.create_task(send_zhuama_shuaxin(data))
                            elif action == 1003:
                                asyncio.create_task(send_zhuama_buhuo(data))
                            elif action == 1007:
                                asyncio.create_task(send_xuanjing(data))
                            elif action == 2001:
                                asyncio.create_task(send_kaifu(data))
                            elif action == 2002:
                                asyncio.create_task(send_xinwen(data))
                            elif action == 1001:
                                asyncio.create_task(send_qiyu(data))
                            elif action == 1004:
                                asyncio.create_task(send_fuyao_kaiqi(data))
                            elif action == 1005:
                                asyncio.create_task(send_fuyao_dianming(data))
                            elif action == 1101:
                                asyncio.create_task(send_gongfang_liangcang(data))
                            elif action == 1102:
                                asyncio.create_task(send_gongfang_dajiang(data))
                            elif action == 1103:
                                asyncio.create_task(send_gongfang_daqi(data))
                            elif action == 1104:
                                asyncio.create_task(send_gongfang_zhanling(data))
                            elif action == 2003:
                                asyncio.create_task(send_gengxin(data))
                            else:
                                pass
                        else:
                            print("close")
                            break
        except Exception as error:
            pass
        if not loop:
            break
        print("链接异常，10s后重新连接")
        await asyncio.sleep(10)


async def send_tieba(data):
    tieba_name = data["name"]
    server_name = data["server"]
    if server_name == "-":
        server_name = ""
    title = data["title"]
    url = data["url"]
    message = f"{title}\n吃瓜地址：{url}\n来源：{tieba_name}\n服务器：{server_name}"
    for send_group_id in await get_group_ids(server_name, "818"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)
    for send_group_id in await get_group_ids(server_name, "818本服"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_zhue(data):
    server_name = data["server"]
    map_name = data["map_name"]
    time = await gettime(data["time"])
    message = f"诛恶事件于{time}触发！众侠士可前往【{map_name}】一探究竟。"
    for send_group_id in await get_group_ids(server_name, "诛恶"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)
        print("诛恶发送成功")


async def send_zhuama_shuaxin(data):
    server_name = data["server"]
    min_time = data["min_time"]
    max_time = data["max_time"]
    map_name = data["map_name"]
    time = await gettime(data["time"])
    message = f"{min_time}-{max_time}分钟后，将有宝马良驹出现在{map_name}\n消息时间{time}"
    for send_group_id in await get_group_ids(server_name, "抓马"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_zhuama_buhuo(data):
    server_name = data["server"]
    player_name = data["name"]
    map_name = data["map_name"]
    horse_name = data["horse"]
    message = f"恭喜玩家{player_name}在{map_name}抓获{horse_name}宝驹。"
    for send_group_id in await get_group_ids(server_name, "抓马"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_kaifu(data):
    server_name = data["server"]
    status = data["status"]
    # time=await gettime(data["date"])
    if status == 1:
        status = "开服"
    else:
        status = "维护"
    message = f"{server_name}已{status}"
    for send_group_id in await get_group_ids(server_name, "开服"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_xinwen(data):
    type = data["type"]
    title = data["title"]
    url = data["url"]
    date = data["date"]
    message = f"{type}来了\n{title}\n{url}\n日期：{date}"
    for send_group_id in await get_group_ids("", "新闻"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_xuanjing(data):
    server_name = data["server"]
    player_name = data["role_name"]
    map_name = data["map_name"]
    xuanjing_name = data["name"]
    message = f"恭喜玩家{player_name}在{map_name}获得{xuanjing_name}。"
    for send_group_id in await get_group_ids(server_name, "玄晶"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_qiyu(data):
    server_name = data["server"]
    player_name = data["name"]
    serendipity = data["event"]
    level = data["level"]
    message = f"恭喜玩家 {player_name} 触发{serendipity}。"
    for send_group_id in await get_group_ids(server_name, "奇遇"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)
    if level == 2:
        for send_group_id in await get_group_ids(server_name, "绝世奇遇"):
            await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_fuyao_kaiqi(data):
    server_name = data["server"]
    time = await gettime(data["time"])
    message = f"[{time}]，扶摇九天已开启"
    for send_group_id in await get_group_ids(server_name, "抓马"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_fuyao_dianming(data):
    server_name = data["server"]
    player_names = data["name"]
    player_names_str = ""
    for i in player_names:
        player_names_str = player_names_str + "【" + i + "】"
    message = f"以下玩家获得扶摇点名:\n{player_names_str}"
    for send_group_id in await get_group_ids(server_name, "抓马"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_gongfang_liangcang(data):
    server_name = data["server"]
    castle = data["castle"]
    camp = data["camp_name"]
    time = await gettime(data["time"])
    message = f"在 {time} {castle} 据点粮仓被一群 {camp} 人士洗劫！"
    for send_group_id in await get_group_ids(server_name, "攻防实况"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_gongfang_dajiang(data):
    server_name = data["server"]
    name = data["name"]
    time = await gettime(data["time"])
    message = f"在 {time} {name} 据点大旗被据点大将重置回初始位置！"
    for send_group_id in await get_group_ids(server_name, "攻防实况"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_gongfang_daqi(data):
    server_name = data["server"]
    castle = data["castle"]
    map = data["map_name"]
    camp = data["camp_name"]
    time = await gettime(data["time"])
    message = f"在 {time} {camp} 位于 {map} 的 {castle} 据点大旗被夺，十分钟后未能夺回大旗，则会丢失此据点！"
    for send_group_id in await get_group_ids(server_name, "攻防实况"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_gongfang_zhanling(data):
    server_name = data["server"]
    castle = data["castle"]
    tong = data["tong_name"]
    camp = data["camp_name"]
    time = await gettime(data["time"])
    message = f"在 {time} {camp} 的 {tong} 帮会成功占领 {castle} 据点！"
    for send_group_id in await get_group_ids(server_name, "攻防实况"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def send_gengxin(data):
    old_version = data["old_version"]
    new_version = data["new_version"]
    package_num = data["package_num"]
    package_size = data["package_size"]
    message = f"游戏更新包已发布，\n{old_version} → {new_version}\n {package_num}个更新包，共{package_size}"
    for send_group_id in await get_group_ids("", "更新"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


async def test(data):
    await get_bot().send_group_msg(group_id=191223830, message=data["serendipity"])


async def gettime(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)

    # 将 datetime 对象格式化为小时:分钟字符串
    formatted_time = dt.strftime("%H:%M")

    return formatted_time


async def wss_close():
    global loop
    if loop:
        await ws_connected.close()
        print("wss链接已关闭")
    loop = False


def setup():
    print()
    # return asyncio.create_task(get_group_ids("绝代天骄","818"))
    return asyncio.create_task(websocket_handler())

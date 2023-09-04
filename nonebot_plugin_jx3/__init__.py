import os
from nonebot.plugin import PluginMetadata
import httpx
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.params import CommandArg
from nonebot import get_driver
from .config import Config
if not os.path.exists("./data"):
    os.mkdir("./data")
from . import subscribe
from .bind import get_bind_server
from .userdefine import emm
__plugin_meta__ = PluginMetadata(
    name="剑网三查询和推送",
    description="是一个使用 NoneBot 框架编写的插件，提供多种剑网三功能如日常查询，预测，金价查询，鲜花，公告，沙盘，jjc，黑市，骚话，奇遇，招募以及多种消息推送功能。",
    usage="剑网三帮助",
    type="application",
    config=Config,
    extra={},
    homepage="https://github.com/fuyang0811/nonebot-plugin-jx3",
    supported_adapters={"~onebot.v11"},
)
api_base_url = "https://www.jx3api.com"
plugin_config = Config.parse_obj(get_driver().config)
robot = plugin_config.jx3_bot_name
head = plugin_config.jx3_command_header
ticket = plugin_config.jx3_tuilan_ticket
token = plugin_config.jx3api_key
from .websocket_handler import wss_close


# global_config = get_driver().config
# config.setup(global_config)
get_driver = get_driver()


@get_driver.on_startup
async def _():
    websocket_handler.setup()
    #zhue.setup2()

@get_driver.on_shutdown
async def _():
    await wss_close()


async def jx3api_request(url, payload):
    async with httpx.AsyncClient() as client:
        response = await client.post(api_base_url + url, params=payload)
    return response.json()


jx3api_help = on_command("剑网三帮助")


@jx3api_help.handle()
async def handle_help():
    await jx3api_help.finish(MessageSegment.image("https://link.jscdn.cn/1drv/aHR0cHM6Ly8xZHJ2Lm1zL2kvcyFBcDJ3X0ZXaUZmRW9nVEVMX3NxOE9IczhST3pUP2U9WUhOY3N0.jpg"))


jx3api_gold_price = on_command(head + "金价")


@jx3api_gold_price.handle()
async def handle_jx3api_gold_price(event, args: Message = CommandArg()):
    if server := args.extract_plain_text():
        pass
    elif server := await get_bind_server(event.group_id):
        pass
    else:
        await jx3api_gold_price.finish("请绑定服务器，或者输入要查询的服务器")

    params = {
        "scale": 1,
        "server": server,
        "robot": robot,
        "cache": 1,
        "token": token
    }
    print(params)
    response = await jx3api_request("/view/trade/demon", params)
    print(response)
    if response["code"] == 200:
        await jx3api_gold_price.finish(MessageSegment.image(response['data']['url']))
    else:
        await jx3api_gold_price.finish("请求出错，请稍后再试")


jx3api_active_today = on_command(head + "日常")


@jx3api_active_today.handle()
async def handle_jx3api_active_today(event, args: Message = CommandArg()):
    if server := args.extract_plain_text():
        pass
    elif server := await get_bind_server(event.group_id):
        pass
    else:
        await jx3api_web_announce.finish("请绑定服务器，或者输入要查询的服务器")

    params = {
        "server": server,
        "num": 0,  # 新增一行，将num参数加入字典
        "robot": robot,
        "cache": 1,
        "token": token
    }
    print(params)
    response = await jx3api_request("/view/active/current", params)  # 修改API的endpoint
    print(response)
    if response["code"] == 200:
        await jx3api_active_today.finish(MessageSegment.image(response['data']['url']))
    else:
        await jx3api_active_today.finish("请求出错，请稍后再试")


jx3api_active_calendar = on_command(head + "预测")


@jx3api_active_calendar.handle()
async def handle_active_calendar(event, args: Message = CommandArg()):
    if server := args.extract_plain_text():
        pass
    elif server := await get_bind_server(event.group_id):
        pass
    else:
        await jx3api_active_calendar.finish("请绑定服务器，或者输入要查询的服务器")

    params = {
        "server": server,
        "num": 7,  # 新增一行，将num参数加入字典
        "robot": robot,
        "cache": 1,
        "token": token
    }
    print(params)
    response = await jx3api_request("/view/active/calendar", params)  # 修改API的endpoint
    print(response)
    if response["code"] == 200:
        await jx3api_active_calendar.finish(MessageSegment.image(response['data']['url']))
    else:
        await jx3api_active_calendar.finish("请求出错，请稍后再试")


jx3api_home_flower = on_command(head + "鲜花")


@jx3api_home_flower.handle()
async def handle_jx3api_home_flower(event, args: Message = CommandArg()):
    if server := args.extract_plain_text():
        pass
    elif server := await get_bind_server(event.group_id):
        pass
    else:
        await jx3api_home_flower.finish("请绑定服务器，或者输入要查询的服务器")

    params = {
        "scale": 1,
        "server": server,
        "robot": robot,
        "cache": 1,
        "token": token
    }
    print(params)
    response = await jx3api_request("/view/home/flower", params)  # 修改API的endpoint
    print(response)
    if response["code"] == 200:
        await jx3api_home_flower.finish(MessageSegment.image(response['data']['url']))
    elif response["code"] == 400:
        await jx3api_home_flower.finish("参数错误")
    elif response["code"] == 404:
        await jx3api_home_flower.finish("未收录")
    else:
        await jx3api_home_flower.finish("请求出错，请稍后再试")


jx3api_web_announce = on_command(head + "公告")


@jx3api_web_announce.handle()
async def handle_web_announce():
    params = {
        "scale": 1,
        "robot": robot,
        "cache": 1,
        "token": token
    }
    print(params)
    response = await jx3api_request("/view/web/announce", params)  # 修改API的endpoint
    print(response)
    if response["code"] == 200:
        await jx3api_web_announce.finish(MessageSegment.image(response['data']['url']))
    else:
        await jx3api_web_announce.finish("请求出错，请稍后再试")


jx3api_server_sand = on_command(head + "沙盘")


@jx3api_server_sand.handle()
async def handle_server_sand(event, args: Message = CommandArg()):
    if server := args.extract_plain_text():
        pass
    elif server := await get_bind_server(event.group_id):
        pass
    else:
        await jx3api_server_sand.finish("请绑定服务器，或者输入要查询的服务器")

    params = {
        "scale": 1,
        "server": server,
        "robot": robot,
        "cache": 1,
        "token": token
    }
    print(params)
    response = await jx3api_request("/view/server/sand", params)  # 修改API的endpoint
    print(response)
    if response["code"] == 200:
        await jx3api_server_sand.finish(MessageSegment.image(response['data']['url']))
    else:
        await jx3api_server_sand.finish("请求出错，请稍后再试")


jx3api_match_recent = on_command(head + "jjc")


@jx3api_match_recent.handle()
async def handle_match_recent(event, args: Message = CommandArg()):
    alldata = args.extract_plain_text().strip().split()
    print(alldata)
    if alldata in [22, 33, 55]:
        pass
    if len(alldata) == 3:
        mode = int(alldata[0])
        server = alldata[1]
        name = alldata[2]
    elif len(alldata) == 2:
        mode = int(alldata[0])
        server = await get_bind_server(event.group_id)
        name = alldata[1]
    else:
        await jx3api_match_recent.finish("参数数量不正确，请参考：-jjc 33 绝代天骄 赤瞳竹，服务器可忽略")

    params = {
        "scale": 1,
        "server": server,
        "name": name,
        "mode": mode,
        "ticket": ticket,
        "robot": robot,
        "token": token
    }
    print(params)
    response = await jx3api_request("/view/match/recent", params)  # 修改API的endpoint
    print(response)
    if response["code"] == 200:
        await jx3api_match_recent.finish(MessageSegment.image(response['data']['url']))
    elif response["code"] == 404:
        await jx3api_match_recent.finish(response["msg"])
    else:
        await jx3api_match_recent.finish("请求出错，请稍后再试")


jx3api_match_school = on_command(head + "jjc统计")


@jx3api_match_school.handle()
async def handle_match_school(event, args: Message = CommandArg()):
    alldata = args.extract_plain_text().strip().split()
    print(alldata)
    if len(alldata) == 1:
        mode = int(alldata[0])
    else:
        await jx3api_match_school.finish("参数数量不正确，请参考：-jjc统计 33")

    params = {
        "mode": mode,
        "ticket": ticket,
        "robot": robot,
        "token": token
    }
    print(params)
    response = await jx3api_request("/view/match/schools", params)  # 修改API的endpoint
    print(response)
    if response["code"] == 200:
        await jx3api_match_school.finish(MessageSegment.image(response['data']['url']))
    elif response["code"] == 404:
        await jx3api_match_school.finish(response["msg"])
    else:
        await jx3api_match_school.finish("请求出错，请稍后再试")


jx3api_heishi = on_command(head + "黑市")


@jx3api_heishi.handle()
async def handle_heishi(event, args: Message = CommandArg()):
    if name := args.extract_plain_text():
        pass
    else:
        await jx3api_heishi.finish("请重新输入，并请输入物品名称")

    params = {
        "scale": 1,
        "name": name,
        "robot": robot,
        "cache": 1,
        "token": token
    }
    print(params)
    response = await jx3api_request("/view/trade/record", params)  # 修改API的endpoint
    print(response)
    if response["code"] == 200:
        await jx3api_heishi.finish(MessageSegment.image(response['data']['url']))
    elif response["code"] == 404 or response["code"] == 400:
        await jx3api_match_recent.finish(response["msg"])
    else:
        await jx3api_heishi.finish("请求出错，请稍后再试")


jx3api_saohua = on_command(head + "骚话")


@jx3api_saohua.handle()
async def handle_saohua(event, args: Message = CommandArg()):
    response = await jx3api_request("/data/saohua/random", {})  # 修改API的endpoint
    print(response)

    if response["code"] == 200:
        await jx3api_saohua.finish(response['data']['text'])
    elif response["code"] == 404 or response["code"] == 400:
        await jx3api_match_recent.finish(response["msg"])
    else:
        await jx3api_saohua.finish("请求出错，请稍后再试")


jx3api_kaifu = on_command(head + "开服")


@jx3api_kaifu.handle()
async def handle_kaifu(event, args: Message = CommandArg()):
    if server := args:
        pass
    else:
        server = await get_bind_server(event.group_id)

    params = {
        "server": server
    }
    response = await jx3api_request("/data/server/check", params)  # 修改API的endpoint
    print(response)
    if response['data']['status']:
        status = server + "已开服"
    else:
        status = server + "维护中"
    if response["code"] == 200:
        await jx3api_kaifu.finish(status)
    elif response["code"] == 404 or response["code"] == 400:
        await jx3api_kaifu.finish(response["msg"])
    else:
        await jx3api_kaifu.finish("请求出错，请稍后再试")
jx3api_qiyu = on_command(head + "奇遇")
@jx3api_qiyu.handle()
async def handle_qiyu(event, args: Message = CommandArg()):
    alldata = args.extract_plain_text().strip().split()
    print(alldata)
    server = await get_bind_server(event.group_id)
    if len(alldata) == 1:
        name = alldata[0]
    else:
        await jx3api_qiyu.finish("参数数量不正确，请参考：-奇遇 赤瞳竹")

    params = {
        "scale": 1,
        "server": server,
        "name": name,
        "filter": 1,
        "robot": robot,
        "ticket": ticket,
        "token": token
    }
    print(params)
    response = await jx3api_request("/view/luck/adventure", params)  # 修改API的endpoint
    print(response)
    if response["code"] == 200:
        await jx3api_qiyu.finish(MessageSegment.image(response['data']['url']))
    elif response["code"] == 404:
        await jx3api_qiyu.finish(response["msg"])
    else:
        await jx3api_qiyu.finish("请求出错，请稍后再试")
jx3api_zhaomu= on_command(head + "招募")
@jx3api_zhaomu.handle()
async def handle_zhaomu(event, args: Message = CommandArg()):
    alldata = args.extract_plain_text().strip().split()
    print(alldata)
    server = await get_bind_server(event.group_id)
    if len(alldata) == 1:
        keyword = alldata[0]
        params = {
            "scale": 1,
            "server": server,
            "keyword": keyword,
            "robot": robot,
            "cache": 1,
            "token": token
        }
    else:
        params = {
            "scale": 1,
            "server": server,
            "robot": robot,
            "cache": 1,
            "token": token
        }


    print(params)
    response = await jx3api_request("/view/member/recruit", params)  # 修改API的endpoint
    print(response)
    if response["code"] == 200:
        await jx3api_zhaomu.finish(MessageSegment.image(response['data']['url']))
    elif response["code"] == 404:
        await jx3api_zhaomu.finish(response["msg"])
    else:
        await jx3api_zhaomu.finish("请求出错，请稍后再试")
async def deal_error(jx3api_handle,response):
    if response["code"]==403:
        await jx3api_handle.finish("请配置jx3api-key")
    elif response["code"] == 404 or response["code"] == 400:
        await jx3api_handle.finish(response["msg"])
    else:
        await jx3api_handle.finish("请求出错，请稍后再试")

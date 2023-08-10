from typing import Optional

from nonebot import get_driver
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from tinydb import TinyDB, Query

from .config import Config
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER

plugin_config = Config.parse_obj(get_driver().config)
robot = plugin_config.jx3_bot_name
head = plugin_config.jx3_command_header
ticket = plugin_config.jx3_tuilan_ticket
token = plugin_config.jx3api_key
subscribes_db = TinyDB("./data/jx3_subscribe.json")
User = Query()
subscribes_name_lib = ["818", "818本服", "更新", "开服", "新闻", "抓马", "扶摇", "诛恶", "阵营活动提醒", "攻防实况",
                       "玄晶", "奇遇", "绝世奇遇"]


async def add_group_id_subscribe(group_id_in: int, subscribe_in: str):
    subscribes_db.insert({"group_id": group_id_in, "subscribe": [subscribe_in]})


async def update_group_id_subscribe(group_id_in: int, new_subscribe_in: list):
    subscribes_db.update({"subscribe": new_subscribe_in}, User.group_id == group_id_in)


async def get_group_id_subscribe(group_id_in: int) -> Optional[list]:
    group_id_subscribe = subscribes_db.search(User.group_id == group_id_in)
    return group_id_subscribe[0]["subscribe"] if group_id_subscribe else None


async def get_subscribe_group(subscribe: str):
    group_servers = subscribes_db.search(User.subscribe.test(lambda s: subscribe in s))
    print(group_servers)
    group_ids = []
    for group_server in group_servers:
        group_ids.append(group_server["group_id"])
    return group_ids


subscribe_event = on_command(head + "订阅", priority=5, permission=GROUP_OWNER | GROUP_ADMIN)


@subscribe_event.handle()
async def handle_bind_server(event, args: Message = CommandArg()):
    if subscribe := args.extract_plain_text():
        if subscribe in subscribes_name_lib:
            pass
        else:
            await subscribe_event.finish(f"请输入正确的订阅内容，订阅如下：{subscribes_name_lib}")
    else:
        old_subscribe = await get_group_id_subscribe(event.group_id)
        if old_subscribe:
            insubscribe = [element for element in subscribes_name_lib if element not in old_subscribe]
        else:
            insubscribe = subscribes_name_lib
        await subscribe_event.finish(f"以下是已订阅内容{old_subscribe}\n"
                                     f"以下是可订阅内容{insubscribe}")
    group_id = event.group_id
    old_subscribe = await get_group_id_subscribe(group_id)
    if old_subscribe is not None:
        if subscribe in old_subscribe:
            await subscribe_event.finish(f"已订阅{subscribe}，无需重复订阅")
        else:
            new_subscribe = old_subscribe + [subscribe]
            await update_group_id_subscribe(group_id, new_subscribe)
    else:
        await add_group_id_subscribe(group_id, subscribe)
    await subscribe_event.finish(f"订阅{subscribe}成功")


cancel_event = on_command(head + "取消订阅", priority=5)


@cancel_event.handle()
async def handel_cancel_event(event, args: Message = CommandArg()):
    if cancel_name := args.extract_plain_text():
        old_subscribe = await get_group_id_subscribe(event.group_id)
        if cancel_name in old_subscribe:
            pass
        else:
            await cancel_event.finish(f"未查询到订阅：{cancel_name}")
    else:
        await cancel_event.finish("请输入取消内容")
    old_subscribe.remove(cancel_name)
    new_subscribe = old_subscribe.copy()
    await update_group_id_subscribe(event.group_id, new_subscribe)
    await cancel_event.finish(f"取消{cancel_name}订阅成功")

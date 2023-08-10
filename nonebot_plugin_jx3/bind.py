from typing import Optional
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from tinydb import TinyDB, Query
from nonebot import get_driver
from .config import Config
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER

plugin_config = Config.parse_obj(get_driver().config)
head = plugin_config.jx3_command_header
bind_servers_db = TinyDB("./data/jx3_bind.json")
User = Query()
server_lib = [""]


async def add_bind_server(group_id_in: int, server_name_in: str):
    bind_servers_db.insert({"group_id": group_id_in, "server": server_name_in})


async def update_bind_server(group_id_in: int, server_name_in: str):
    bind_servers_db.update({"server": server_name_in}, User.group_id == group_id_in)


async def get_bind_server(group_id_in: int) -> Optional[str]:
    bind_server = bind_servers_db.search(User.group_id == group_id_in)
    print(bind_server)
    return bind_server[0]["server"] if bind_server else None


async def get_bind_group(server: str):
    group_servers = bind_servers_db.search(User.server == server)
    group_ids = []
    for group_server in group_servers:
        group_ids.append(group_server["group_id"])
    return group_ids


bind_server = on_command(head + "绑定", priority=5, permission=GROUP_OWNER | GROUP_ADMIN)


@bind_server.handle()
async def handle_bind_server(event, args: Message = CommandArg()):
    if server := args.extract_plain_text():
        pass
    else:
        await bind_server.finish("请输入服务器名称")
    group_id = event.group_id
    server_name = server
    if await get_bind_server(group_id):
        await update_bind_server(group_id, server_name)
    else:
        await add_bind_server(group_id, server_name)
    await bind_server.finish(f"已将该群组绑定至{server_name}服务器")

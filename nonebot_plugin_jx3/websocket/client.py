"""WebSocket 连接管理"""
import asyncio

from aiohttp import ClientSession, ClientTimeout
from nonebot import logger


_ws = None        # WebSocket 连接对象
_running = False  # 运行标志


async def start():
    """启动 WebSocket 连接"""
    global _running
    _running = True
    asyncio.create_task(_connect_loop())


async def close():
    """关闭 WebSocket 连接"""
    global _running, _ws
    _running = False
    if _ws:
        await _ws.close()
        logger.info("[JX3] WebSocket 已关闭")


async def _connect_loop():
    """带自动重连的连接循环，指数退避（最大60s）"""
    global _ws
    from ..config import plugin_config

    retry_delay = 5

    while _running:
        try:
            headers = {"token": plugin_config.jx3wss_token} if plugin_config.jx3wss_token else {}
            async with ClientSession(timeout=ClientTimeout(total=10)) as session:
                async with session.ws_connect(
                    plugin_config.jx3_wss_url,
                    headers=headers,
                    ssl=True
                ) as ws:
                    _ws = ws
                    retry_delay = 5  # 连接成功，重置退避
                    logger.info("[JX3] WebSocket 连接成功")

                    async for msg in ws:
                        if msg.type == 1:  # TEXT
                            data = msg.json()
                            asyncio.create_task(_dispatch(data))
                        else:
                            break

        except Exception as e:
            logger.error(f"[JX3] WebSocket 异常: {e}")

        if not _running:
            break
        logger.info(f"[JX3] {retry_delay}s 后重连...")
        await asyncio.sleep(retry_delay)
        retry_delay = min(retry_delay * 2, 60)


async def _dispatch(msg: dict):
    """按 action 分发到 handlers"""
    from .handlers import HANDLER_MAP

    action = msg.get("action")
    if action == 10000:  # 心跳
        return

    # 新API格式：数据在 detail 字段中，旧格式在 data 字段中
    detail = msg.get("detail", msg.get("data", {}))

    handler = HANDLER_MAP.get(action)
    if handler:
        try:
            await handler(action, detail)
        except Exception as e:
            logger.error(f"[JX3] 处理事件 {action} 出错: {e}")
    else:
        logger.debug(f"[JX3] 未处理的事件: action={action}")

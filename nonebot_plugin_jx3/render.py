"""HTML→图片渲染引擎"""
import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from nonebot_plugin_htmlrender import html_to_pic

TEMPLATE_DIR = Path(__file__).parent / "templates"


def _format_ts(value):
    """Jinja2 过滤器：Unix 时间戳 → 可读日期"""
    try:
        ts = int(value)
        dt = datetime.datetime.fromtimestamp(ts)
        return dt.strftime("%m-%d %H:%M")
    except (ValueError, TypeError, OSError):
        return str(value)


class JX3Renderer:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(str(TEMPLATE_DIR)),
            autoescape=True
        )
        self.env.filters["format_ts"] = _format_ts

    async def render(self, template_name: str, **kwargs) -> bytes:
        """渲染 Jinja2 模板为 PNG 图片字节。

        Args:
            template_name: 模板文件名，如 "calendar.html"
            **kwargs: 传递给模板的数据

        Returns:
            PNG 图片的 bytes
        """
        from .config import plugin_config

        # 注入公共变量
        kwargs.setdefault("bot_name", plugin_config.jx3_bot_name)
        kwargs.setdefault("timestamp", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        template = self.env.get_template(template_name)
        html = template.render(**kwargs)
        
        if "sand" in template_name:
            view_width = 1297
        elif "gold_trend" in template_name:
            view_width = 660
        else:
            view_width = 600
        
        return await html_to_pic(
            html,
            viewport={"width": view_width, "height": 10},
            wait=0,
            template_path=f"file://{TEMPLATE_DIR.as_posix()}",
        )


# 模块级单例
renderer = JX3Renderer()

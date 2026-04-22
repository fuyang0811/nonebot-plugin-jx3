"""HTTP API 客户端 — 封装所有 JX3API 端点"""
import httpx
from typing import Optional

from nonebot import logger


class JX3APIError(Exception):
    """API 请求错误"""
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(f"[{code}] {msg}")


class JX3APIClient:
    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None
        self.base_url = ""
        self.token = ""
        self.ticket = ""

    def init_config(self):
        """延迟初始化配置，避免启动时循环导入"""
        from .config import plugin_config
        self.base_url = plugin_config.jx3api_base_url
        self.token = plugin_config.jx3api_key
        self.ticket = plugin_config.jx3_tuilan_ticket

    async def start(self):
        """启动 HTTP 客户端"""
        self.init_config()
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=15.0
        )
        logger.info("[JX3] HTTP API 客户端已启动")

    async def close(self):
        """关闭 HTTP 客户端"""
        if self._client:
            await self._client.aclose()
            logger.info("[JX3] HTTP API 客户端已关闭")

    async def _request(self, endpoint: str, **params) -> dict:
        """统一请求方法。
        - 自动注入 token（如果有）
        - 自动注入 ticket（如果有）
        - 统一错误处理
        - 返回 data 字段
        """
        if self.token:
            params.setdefault("token", self.token)
        if self.ticket:
            params.setdefault("ticket", self.ticket)

        # 移除空字符串参数
        params = {k: v for k, v in params.items() if v != ""}

        try:
            resp = await self._client.post(endpoint, json=params)
            result = resp.json()
        except Exception as e:
            raise JX3APIError(0, f"请求异常：{e}")

        if result["code"] != 200:
            raise JX3APIError(result["code"], result.get("msg", "未知错误"))

        return result["data"]

    # ============================================================
    # 免费接口 (USER)
    # ============================================================

    async def active_calendar(self, server: str = "", num: int = 0) -> dict:
        """活动日历。查询日常任务活动。
        endpoint: /data/active/calendar
        params: server(可选), num(0=今天,1=明天,2=后天)
        """
        return await self._request("/data/active/calendar", server=server, num=num)

    async def active_list_calendar(self, num: int = 0) -> dict:
        """活动月历。查询当月/下月活动月历。
        endpoint: /data/active/list/calendar
        params: num(0=本月,1=下月)
        """
        params = {} if num == 0 else {"num": num}
        return await self._request("/data/active/list/calendar", **params)

    async def active_celebs(self, name: str = "") -> dict:
        """行侠事件。查询行侠仗义进行中的事件。
        endpoint: /data/active/celebs
        params: name(可选，NPC名称)
        """
        return await self._request("/data/active/celebs", name=name)

    async def exam_search(self, subject: str, limit: int = 10) -> list:
        """科举答题。搜索科举试题答案。
        endpoint: /data/exam/search
        params: subject(题目关键字), limit(数量,默认10)
        """
        return await self._request("/data/exam/search", subject=subject, limit=limit)

    async def home_flower(self, server: str, name: str = "", map: str = "") -> dict:
        """家园鲜花。查询鲜花最高价格和采集线路。
        endpoint: /data/home/flower
        params: server(必须), name(鲜花名,可选), map(地图名,可选)
        """
        return await self._request("/data/home/flower", server=server, name=name, map=map)

    async def home_furniture(self, name: str) -> dict:
        """家园装饰。查询装饰图纸信息。
        endpoint: /data/home/furniture
        params: name(装饰名称)
        """
        return await self._request("/data/home/furniture", name=name)

    async def home_travel(self, name: str) -> dict:
        """器物图谱。查询器物图谱信息。
        endpoint: /data/home/travel
        params: name(器物名称)
        """
        return await self._request("/data/home/travel", name=name)

    async def news_allnews(self, limit: int = 10) -> list:
        """新闻资讯。获取最新官方新闻列表。
        endpoint: /data/news/allnews
        params: limit(数量,默认10)
        """
        return await self._request("/data/news/allnews", limit=limit)

    async def news_announce(self, limit: int = 5) -> list:
        """维护公告。获取最新维护与更新公告。
        endpoint: /data/news/announce
        params: limit(数量,默认5)
        """
        return await self._request("/data/news/announce", limit=limit)

    async def master_search(self, name: str) -> dict:
        """搜索区服。模糊搜索区服信息。
        endpoint: /data/master/search
        params: name(搜索关键字)
        """
        return await self._request("/data/master/search", name=name)

    async def status_check(self, server: str) -> dict:
        """开服状态。查询服务器维护/开服/繁忙/爆满状态。
        endpoint: /data/status/check
        params: server(服务器名)
        返回: {"zone":"电信区","server":"长安城","status":"爆满"}
        """
        return await self._request("/data/status/check", server=server)

    async def skill_rework(self, name: str) -> dict:
        """技改记录。查询指定心法的技能调整记录。
        endpoint: /data/skill/rework
        params: name(心法名称)
        """
        return await self._request("/data/skill/rework", name=name)

    async def school_foods(self, name: str) -> dict:
        """小药推荐。查询指定心法的推荐小药。
        endpoint: /data/school/foods
        params: name(心法名称)
        """
        return await self._request("/data/school/foods", name=name)

    # ============================================================
    # VIP 接口（需 token）
    # ============================================================

    async def active_monster(self) -> dict:
        """百战首领。查询本周百战异闻录首领。
        endpoint: /data/active/monster
        """
        return await self._request("/data/active/monster")

    async def active_next_event(self) -> dict:
        """扶摇预测。预测下一次扶摇九天会出现的奇遇。
        endpoint: /data/active/next/event
        """
        return await self._request("/data/active/next/event")

    async def auction_records(self, server: str) -> dict:
        """阵营拍卖。查询服务器阵营拍卖记录。
        endpoint: /data/auction/records
        params: server
        """
        return await self._request("/data/auction/records", server=server)

    async def steed_records(self, server: str) -> dict:
        """的卢记录。查询服务器的的卢捕获记录。
        endpoint: /data/steed/records
        params: server
        """
        return await self._request("/data/steed/records", server=server)

    async def show_records(self, server: str, name: str) -> dict:
        """烟花记录。查询角色的烟花记录。
        endpoint: /data/show/records
        params: server, name(角色名)
        """
        return await self._request("/data/show/records", server=server, name=name)

    async def fraud_detail(self, uin: int) -> dict:
        """骗子查询。查询QQ号是否在骗子库中。
        endpoint: /data/fraud/detail
        params: uin(QQ号)
        """
        return await self._request("/data/fraud/detail", uid=uin)

    async def event_records(self, server: str, name: str) -> list:
        """角色奇遇。查询角色触发的奇遇记录。
        endpoint: /data/event/records
        params: server, name(角色名)
        """
        return await self._request("/data/event/records", server=server, name=name)

    async def event_unfinished(self, server: str, name: str) -> list:
        """未做奇遇。查询角色未完成的奇遇。
        endpoint: /data/event/unfinished
        params: server, name(角色名)
        """
        return await self._request("/data/event/unfinished", server=server, name=name)

    async def event_recent(self, server: str) -> list:
        """近期奇遇。查询服务器近期触发的奇遇。
        endpoint: /data/event/recent
        params: server
        """
        return await self._request("/data/event/recent", server=server)

    async def event_statistics(self, server: str, name: str = "") -> dict:
        """奇遇统计。统计奇遇触发频率。
        endpoint: /data/event/statistics
        params: server, name(可选，奇遇名)
        """
        return await self._request("/data/event/statistics", server=server, name=name)

    async def event_collect(self, server: str, num: int = 7) -> list:
        """奇遇汇总。汇总近N天奇遇触发。
        endpoint: /data/event/collect
        params: server, num(天数，默认7)
        """
        return await self._request("/data/event/collect", server=server, num=num)

    async def arena_recent(self, server: str, name: str, mode: int = 33) -> dict:
        """名剑战绩。查询角色名剑大会战绩。需要 ticket。
        endpoint: /data/arena/recent
        params: server, name, mode(22/33/55), ticket, token
        """
        return await self._request("/data/arena/recent", server=server, name=name, mode=mode)

    async def arena_awesome(self, mode: int = 33) -> list:
        """名剑排行。查询名剑大会排行榜。需要 ticket。
        endpoint: /data/arena/awesome
        params: mode(22/33/55), ticket, token
        """
        return await self._request("/data/arena/awesome", mode=mode)

    async def arena_schools(self, mode: int = 33) -> list:
        """名剑统计。统计门派名剑大会排名。需要 ticket。
        endpoint: /data/arena/schools
        params: mode(22/33/55), ticket, token
        """
        return await self._request("/data/arena/schools", mode=mode)

    async def recruit_search(self, server: str, keyword: str = "", type: int = 1) -> dict:
        """团队招募。查询团队招募信息。
        endpoint: /data/recruit/search
        params: server, keyword(可选), type(1=本服+跨服, 2=本服, 3=跨服)
        """
        return await self._request("/data/recruit/search", server=server, keyword=keyword, type=type)

    async def mentor_search(self, server: str, keyword: str = "") -> dict:
        """师徒系统。查询师徒招募信息。
        endpoint: /data/mentor/search
        params: server, keyword(可选)
        """
        return await self._request("/data/mentor/search", server=server, keyword=keyword)

    async def rank_statistical(self, server: str, type: str = "个人") -> list:
        """本服榜单。查询服务器各类榜单。
        endpoint: /data/rank/statistical
        params: server, type(榜单类型)
        """
        return await self._request("/data/rank/statistical", server=server, type=type)

    async def reward_statistics(self, server: str, name: str) -> dict:
        """掉落统计。统计副本装备掉落。
        endpoint: /data/reward/statistics
        params: server, name(副本名)
        """
        return await self._request("/data/reward/statistics", server=server, name=name)

    async def role_detail(self, server: str, name: str) -> dict:
        """角色信息。查询角色详细信息。
        endpoint: /data/role/detail
        params: server, name(角色名)
        """
        return await self._request("/data/role/detail", server=server, name=name)

    async def card_record(self, server: str, name: str) -> dict:
        """角色名片。获取角色最新名片。
        endpoint: /data/card/record
        params: server, name(角色名)
        """
        return await self._request("/data/card/record", server=server, name=name)

    async def card_records(self, server: str, name: str) -> list:
        """所有名片。获取角色历史名片列表。
        endpoint: /data/card/records
        params: server, name(角色名)
        """
        return await self._request("/data/card/records", server=server, name=name)

    async def card_cached(self, server: str, name: str) -> dict:
        """缓存名片。获取角色缓存名片（速度更快）。
        endpoint: /data/card/cached
        params: server, name(角色名)
        """
        return await self._request("/data/card/cached", server=server, name=name)

    async def role_monster(self, server: str, name: str) -> dict:
        """角色百战。查询角色百战异闻录进度。
        endpoint: /data/role/monster
        params: server, name(角色名)
        """
        return await self._request("/data/role/monster", server=server, name=name)

    async def school_matrix(self, name: str) -> dict:
        """心法阵眼。查询心法的阵眼效果。
        endpoint: /data/school/matrix
        params: name(心法名)
        """
        return await self._request("/data/school/matrix", name=name)

    async def school_talent(self, name: str) -> dict:
        """奇穴详情。查询心法奇穴。
        endpoint: /data/school/talent
        params: name(心法名)
        """
        return await self._request("/data/school/talent", name=name)

    async def school_skills(self, name: str) -> dict:
        """技能详情。查询心法技能列表。
        endpoint: /data/school/skills
        params: name(心法名)
        """
        return await self._request("/data/school/skills", name=name)

    async def school_seniority(self, server: str, school: str = "") -> list:
        """资历排行。查询服务器资历排行。
        endpoint: /data/school/seniority
        params: server, school(心法名,可选)
        """
        return await self._request("/data/school/seniority", server=server, school=school)

    async def sand_records(self, server: str) -> dict:
        """阵营沙盘。查询沙盘据点信息。
        endpoint: /data/sand/records
        params: server
        """
        return await self._request("/data/sand/records", server=server)

    async def fenxian_records(self, server: str) -> list:
        """阵营事件。查询阵营事件记录。
        endpoint: /data/fenxian/records
        params: server
        """
        return await self._request("/data/fenxian/records", server=server)

    async def smite_records(self, server: str) -> list:
        """诛恶事件。查询服务器诛恶记录。
        endpoint: /data/smite/records
        params: server
        """
        return await self._request("/data/smite/records", server=server)

    async def mine_cart(self, server: str = "") -> dict:
        """关隘首领。查询关隘首领信息。
        endpoint: /data/mine/cart
        params: server(可选)
        """
        return await self._request("/data/mine/cart", server=server)

    async def chitu_records(self, server: str) -> list:
        """本日赤兔。查询今日赤兔刷新记录。
        endpoint: /data/chitu/records
        params: server
        """
        return await self._request("/data/chitu/records", server=server)

    async def chitu_week_records(self, server: str) -> list:
        """本周赤兔。查询本周赤兔刷新记录。
        endpoint: /data/chitu/week/records
        params: server
        """
        return await self._request("/data/chitu/week/records", server=server)

    async def ranch_records(self, server: str) -> list:
        """马场刷新。查询马场刷新记录。
        endpoint: /data/ranch/records
        params: server
        """
        return await self._request("/data/ranch/records", server=server)

    async def rank_trials(self, server: str, school: str = "") -> list:
        """试炼排行。查询试炼之地排行。
        endpoint: /data/rank/trials
        params: server, school(心法名,可选)
        """
        return await self._request("/data/rank/trials", server=server, name=school)

    async def tieba_item_records(self, name: str, server: str = "") -> dict:
        """贴吧物价。查询贴吧物价信息。
        endpoint: /data/tieba/item/records
        params: name(物品名), server(可选)
        """
        return await self._request("/data/tieba/item/records", name=name, server=server)

    async def trade_demon(self, server: str, limit: int = 30) -> list:
        """金币价格。查询金价比例。
        endpoint: /data/trade/demon
        params: server, limit(默认30)
        返回: [{"zone","server","tieba","wanbaolou","dd373","date"}]
        """
        return await self._request("/data/trade/demon", server=server, limit=limit)

    async def trade_records(self, name: str, server: str = "") -> dict:
        """黑市物价。查询黑市交易记录。
        endpoint: /data/trade/records
        params: name(物品名), server(可选)
        """
        return await self._request("/data/trade/records", name=name, server=server)

    async def trade_item_search(self, name: str) -> list:
        """搜索物品。搜索黑市物品。
        endpoint: /data/trade/item/search
        params: name(搜索关键字)
        """
        return await self._request("/data/trade/item/search", name=name)

    async def trade_item_records(self, name: str, server: str = "") -> dict:
        """物品价格。查询万宝楼物品价格趋势。
        endpoint: /data/trade/item/records
        params: name(物品名), server(可选)
        """
        return await self._request("/data/trade/item/records", name=name, server=server)

    async def battle_records(self, server: str) -> dict:
        """帮战记录。查询服务器帮战记录。
        endpoint: /data/battle/records
        params: server
        """
        return await self._request("/data/battle/records", server=server)

    async def mech_calculator(self, name: str) -> dict:
        """副本解密。查询副本解密答案。
        endpoint: /data/mech/calculator
        params: name(副本名)
        """
        return await self._request("/data/mech/calculator", name=name)

    async def duowan_statistics(self, server: str) -> dict:
        """统战歪歪。查询歪歪统战频道。
        endpoint: /data/duowan/statistics
        params: server
        """
        return await self._request("/data/duowan/statistics", server=server)

    # ============================================================
    # 其他免费接口
    # ============================================================

    async def tieba_random(self, tags: str = "818") -> dict:
        """八卦帖子。随机一条八卦帖子。
        endpoint: /data/tieba/random
        返回: {"id","class","server","title","url","date"}
        """
        return await self._request("/data/tieba/random", tags=tags)

    async def saohua_random(self) -> dict:
        """世界骚话。随机一条骚话。
        endpoint: /data/saohua/random
        返回: {"id","text"}
        """
        return await self._request("/data/saohua/random")

    async def saohua_content(self) -> dict:
        """舔狗日记。随机一条舔狗日记。
        endpoint: /data/saohua/content
        返回: {"id","text"}
        """
        return await self._request("/data/saohua/content")


# 模块级单例
api_client = JX3APIClient()

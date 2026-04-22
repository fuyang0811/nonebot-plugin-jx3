<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-jx3

_基于 [NoneBot2](https://github.com/nonebot/nonebot2) 的剑网三（JX3）全功能 QQ 群助手插件，支持游戏数据查询与实时推送通知。_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/fuyang0811/nonebot-plugin-jx3.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-jx3">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-jx3.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## ✨ v1.0 完全重写

本版本基于 v0.x 进行了**完全重写**，主要变化：

- **架构重构**：采用模块化设计，代码按功能拆分为独立模块（`commands/`、`websocket/`、`templates/`）
- **API 升级**：全面迁移至 JX3API 最新 JSON 接口
- **配置系统**：基于 Pydantic v2 的类型安全配置，支持热加载
- **图片渲染**：使用 Jinja2 + HTML 模板引擎渲染查询结果，输出更精美
- **WebSocket 推送**：重写事件驱动架构，支持断线自动重连（指数退避，5s~60s）
- **数据存储**：使用 TinyDB 轻量级本地数据库，替代原有 JSON 文件方案

## 功能概览

- **数据查询**：日常、金价、角色、心法、奇遇、招募、科举等 40+ 指令
- **实时推送**：奇遇、抓马、开服、新闻、攻防实况等 30+ 事件订阅
- **图片渲染**：所有查询结果以精美图片形式输出

## 安装

使用 nb-cli 安装（推荐）：

```bash
nb plugin install nonebot-plugin-jx3
```

或使用 pip：

```bash
pip install nonebot-plugin-jx3
```

**依赖**：`nonebot_plugin_apscheduler`、`nonebot_plugin_htmlrender`、`nonebot_plugin_localstore`、`httpx`、`aiohttp`、`tinydb`

## 配置

在 `.env` 文件中添加以下配置项：

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `jx3api_key` | `""` | HTTP API token（VIP 接口需要）|
| `jx3_tuilan_ticket` | `""` | 推栏 ticket（JJC/名剑大会接口需要）|
| `jx3wss_token` | `""` | WebSocket token（推送功能需要）|
| `jx3_enabled_groups` | `[]` | 群白名单，空列表表示所有群均可使用 |
| `jx3_bot_name` | `"水水"` | API 生成图片中显示的机器人名称 |
| `jx3api_base_url` | `https://www.jx3api.com` | HTTP API 地址 |
| `jx3_wss_url` | `wss://seasun.nicemoe.com` | WebSocket 地址 |
| `jx3_default_server` | `""` | 群未绑定时的默认服务器 |

## 使用方法

### 初始设置（群管理员/群主）

```
绑定 <服务器名>     # 绑定本群服务器，例：绑定 绝代天骄
订阅               # 查看可订阅的推送列表
订阅 <名称>        # 开启订阅，例：订阅 奇遇
取消订阅 <名称>    # 关闭订阅
```

### 指令列表

**基础信息**

| 指令 | 说明 |
|---|---|
| `剑三帮助` | 显示帮助图片 |
| `日常 [服务器]` | 今日日常任务 |
| `预测 [服务器]` | 明日日常预测 |
| `月历` | 本月活动日历 |
| `行侠 [NPC]` | 行侠仗义事件 |
| `开服 [服务器]` | 服务器开关状态 |
| `搜服 <名称>` | 搜索服务器 |
| `新闻` | 最新游戏新闻 |
| `公告` | 维护公告 |

**交易市场**

| 指令 | 说明 |
|---|---|
| `金价 [服务器]` | 金币汇率及趋势图 |
| `黑市 <物品>` | 黑市物价查询 |
| `物价 <物品>` | 万宝楼物价趋势 |
| `搜索物品 <名称>` | 物品搜索 |
| `贴吧物价 <物品>` | 贴吧物价 |

**角色查询**

| 指令 | 说明 |
|---|---|
| `角色 <名称>` | 角色详情 |
| `名片 <角色>` | 角色名片 |
| `jjc <角色>` | 名剑大会战绩（需 ticket）|
| `烟花 <角色>` | 烟花记录 |
| `奇遇 <角色>` | 奇遇记录 |
| `未做奇遇 <角色>` | 未完成奇遇 |
| `近期奇遇` | 服务器近期奇遇 |
| `奇遇统计 [奇遇名]` | 奇遇统计 |
| `奇遇汇总` | 奇遇汇总 |

**心法/玩法**

| 指令 | 说明 |
|---|---|
| `小药 <心法>` | 推荐小药配置 |
| `技改 <心法>` | 技能改动历史 |
| `阵眼 <心法>` | 阵眼效果 |
| `奇穴 <心法>` | 奇穴详情 |
| `技能 <心法>` | 技能列表 |
| `资历 [心法]` | 资历榜单 |
| `科举 <题目>` | 科举答题 |

**家园/其他**

| 指令 | 说明 |
|---|---|
| `鲜花 [服务器]` | 家园鲜花价格 |
| `装饰 <名称>` | 家园装饰图纸 |
| `图谱 <名称>` | 行旅图谱 |
| `招募 [关键字]` | 团队招募 |
| `师徒 [关键字]` | 师徒系统 |
| `沙盘 [服务器]` | 阵营沙盘地图 |
| `帮战` | 帮会战绩 |
| `百战` | 百战异闻录 |
| `骚话` | 随机骚话 |
| `舔狗` | 舔狗日记 |
| `八卦` | 随机八卦 |

### 推送订阅列表

| 订阅名称 | 说明 |
|---|---|
| `奇遇` / `绝世奇遇` | 玩家触发奇遇 |
| `抓马` | 马匹刷新/捕获 |
| `扶摇` | 扶摇九天开启/点名 |
| `烟花` | 烟花发送 |
| `的卢` | 的卢刷新/捕获/拍卖 |
| `玄晶` | 玄晶获取 |
| `阵营拍卖` | 阵营拍卖更新 |
| `诛恶` | 诛恶事件 |
| `追魂` | 追魂点名 |
| `祭天` | 阵营祭天 |
| `攻防实况` | 帮战宣战/结果/详情 |
| `开服` | 服务器开关服 |
| `新闻` | 游戏新闻 |
| `更新` | 游戏更新 |
| `818` | 八卦推送 |
| `关隘` | 关隘 BOSS 事件 |
| `云丛` | 云丛预告 |

## 接口说明

- **免费接口**：无需任何 token 即可使用
- **VIP 接口**：需要 `jx3api_key`（购买地址：[jx3api.com](https://www.jx3api.com)）
- **JJC 接口**：额外需要 `jx3_tuilan_ticket`
- **推送功能**：需要 `jx3wss_token`，WebSocket 断线自动重连（5s 起步，最大 60s）

## 致谢

- 感谢 绝代天骄-白首亦同归 帮主 赞助 api 测试。
- 感谢 [jx3-help](https://github.com/abandon-jw3/jx3-help) 项目提供的沙盘资源库。

## 开发者

water · QQ: 415276785

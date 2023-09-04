<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-jx3

_这是一个使用 NoneBot 框架编写的插件，提供多种功能如日常查询，预测，金价查询，鲜花，公告，沙盘，jjc，黑市，骚话，奇遇，招募以及多种消息推送功能。_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/water/nonebot-plugin-jx3.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-jx3">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-jx3.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>


## 📖 介绍

nonebot-plugin-jx3 是一个使用 NoneBot 框架编写的插件，它提供了多种功能，例如日常查询，预测，金价查询，鲜花，公告，沙盘，jjc，黑市，骚话，奇遇，招募以及多种消息推送功能，例如"818", "开服", "新闻", "抓马", "扶摇", "诛恶", "阵营活动提醒", "攻防实况", "玄晶","奇遇","绝世奇遇" 等。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-jx3

</details>

<details>
<summary>手动安装</summary>
将 none-plugin-jx3 文件夹复制到你的 NoneBot 项目的 plugins 目录下。

在你的 NoneBot 配置文件中，添加插件的导入路径：

plugin_dirs = ["plugins"]

将requirements.txt复制到bot目录，进入bot的虚拟环境，执行：

    pip install -r requirements.txt

安装完成后正常启动bot即可
</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:--:|:---:|:----:|
| jx3api_key | 否  |  空  | jx3api.com购买的key（jx3api.com已开启全站鉴权，所有主动查询功能都需要key。 |
| jx3_tuilan_ticket | 否  |  空  | 推栏ticket |
| jx3wss_token| 否  |  空  | jx3api.com购买的wss |
| jx3_command_header | 否  |  空  | 指令的前缀，防止和其他插件冲突 |
| jx3_bot_name | 否  | 团团  | api生成图片用的名字 |

第一步使用插件是要绑定服务器。例如：绑定 绝代天骄

一旦服务器是绑定的，就可以使用各种查询功能。通过-订阅，你可以查询能够订阅的功能。
## 指令示例

| 指令 |                      参数                       |             指令示例              | 说明 |
|:-----:|:---------------------------------------------:|:-----------------------------:|:----:|
| 剑网三帮助 |                       无                       |             剑网三帮助             | 获取剑网三插件的帮助信息 |
| 绑定 |                 服务器（建议进群运行一次）                 |            绑定 绝代天骄            | 将服务器绑定到群组 |
| 日常 |                       无                       |         日常<br>日常 绝代天骄         | 获取今天的日常 |
| 预测|                       无                       |         预测<br>预测 绝代天骄         | 获取明天的日常 |
| 金价 |               服务器（可省略，默认取绑定服务器）               |         金价<br>金价 绝代天骄         | 获取过去两周的服务器金价 |
| 鲜花 |               服务器（可省略，默认取绑定服务器）               |         鲜花<br>鲜花 绝代天骄         | 获取过去两周的服务器鲜花价格 |
| 公告 |                       无                       |         公告<br>公告 绝代天骄         | 获取最新的公告 |
| 沙盘 |               服务器（可省略，默认取绑定服务器）               |         沙盘<br>沙盘 绝代天骄         | 获取服务器沙盘 |
| jjc |   模式（22、33、55）<br>服务器（可省略，默认取绑定服务器）<br>角色名    | jjc 22 绝代天骄 xxx<br>jjc 22 xxx | 获取jjc战绩 |
| 黑市 |                   时装名称（必填）                    |             黑市 狐金             | 获取时装价格 |
| 骚话 |                       无                       |              骚话               | 随即一条骚话 |
| 奇遇 |         服务器（可省略，默认取绑定服务器）<br>角色名（必填）          |     奇遇 xxx<br>奇遇 绝代天骄 xxx     | 获取角色奇遇记录 |
| 招募 | 服务器（可省略，默认取绑定服务器）<br>关键词（支持模糊搜索，可省略，省略返回所有招募） |      招募 名剑<br>招募 绝代天骄 名剑      | 获取服务招募 |
| 订阅 | 开服（维护和开服提醒）<br>新闻（服务器新闻公告推送）<br>更新（游戏更新包发布推送）<br>818本服（本服贴吧和剑网三贴吧的818帖子推送）<br>818（所有服务器贴吧和剑网三贴吧的818帖子推送）<br>后面的功能都需要jx3wss_token <br>诸恶（服务器诸恶刷新提醒）<br>攻防实况（服务器攻防状态推送，包括大将，占领等）<br>阵营活动提醒（服务器阵营活动提醒，提前半小时提醒攻防等）<br>绝世奇遇（服务器绝世奇遇触发提醒）<br>奇遇（服务器奇遇触发提醒）<br>抓马（服务器马匹刷新和被捕获推送）<br>玄晶（服务器获取玄晶推送）|      订阅 开服      | 订阅推送服务 |

开发者:water

qq:415276785

感谢 绝代天骄-白首亦同归-帮主 赞助api测试。

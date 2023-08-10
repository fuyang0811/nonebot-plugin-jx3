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
将插件文件夹复制到你的 NoneBot 项目的 plugins 目录下。

在你的 NoneBot 配置文件中，添加插件的导入路径，例如：

nonebot.load_plugins("plugins.nonebot_plugin_jx3")

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:--:|:---:|:----:|
| jx3api_key | 否  |  空  | jx3.api.com购买的key |
| jx3_tuilan_ticket | 否  |  空  | 推栏ticket |
| jx3wss_token| 否  |  空  | jx3.api.com购买的wss |
| jx3_command_header | 否  |  空  | 指令的前缀，防止和其他插件冲突 |
| jx3_bot_name | 否  | 团团  | api生成图片用的名字 |

第一步使用插件是要绑定服务器。例如：-绑定 绝代天骄

一旦服务器是绑定的，就可以使用各种查询功能。通过-订阅，你可以查询能够订阅的功能。

开发者:water

qq:415276785

import csv
import os

from nonebot import on_command, require, get_bot
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.params import CommandArg

from .websocket_handler import get_group_ids

"""filename = "qiyu.csv"
filename = os.path.join(os.path.dirname(__file__), 'data', f'{filename}')
qiyu_urls = {}
head = "-"
with open(filename, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # skip header row
    for row in reader:
        qiyu_urls[row[0]] = row[1]

jx3api_gonglue = on_command(head + "攻略")


@jx3api_gonglue.handle()
async def handle_gonglue(event, args: Message = CommandArg()):
    if name := args.extract_plain_text():
        pass
    else:
        await jx3api_gonglue.finish(f"攻略指令示例：{head}+攻略 阴阳两界")
    text_path = os.path.join(os.path.dirname(__file__), 'data', 'qiyu', f'{name}.txt')
    image_path = os.path.join(os.path.dirname(__file__), 'data', 'qiyu', f'{name}.jpg')
    if os.path.isfile(image_path):
        image = MessageSegment.image('file:///' + image_path)
    else:
        print(f'{filename} does not exist')
        image_files = os.listdir(os.path.join(os.path.dirname(__file__), 'data', 'qiyu', f'{name}'))
        image = ""
        for image_file in image_files:
            image = image + MessageSegment.image(
                "file:///" + os.path.join(os.path.dirname(__file__), 'data', 'qiyu', f'{name}', image_file))
    with open(text_path, encoding="utf-8") as emmm:
        textlist = emmm.readlines()
        text = ""
        for i in textlist:
            text = text + i
    await jx3api_gonglue.finish(text + image + qiyu_urls[name])

"""
scheduler = require("nonebot_plugin_apscheduler").scheduler
print("攻防订阅加载")

async def send_gongfang_message(message):
    print(message)
    for send_group_id in await get_group_ids("", "阵营活动提醒"):
        await get_bot().send_group_msg(group_id=send_group_id, message=message)


# 在周二和周四的 19:20 发送消息
scheduler.add_job(send_gongfang_message, "cron", day_of_week="1,3", hour=19, minute=20,
                  args=["阵营小攻防将在20：00开始，将在19：28排队。"])
# 在周六和周日的 11:50 和 17:50 发送消息
scheduler.add_job(send_gongfang_message, "cron", day_of_week="5,6", hour=18, minute=20,
                  args=["阵营攻防将在19：00开始，将在18：30排队。"])
scheduler.add_job(send_gongfang_message, "cron", day_of_week="5,6", hour=12, minute=20,
                  args=["阵营攻防将在13：00开始，将在12：30排队。"])
scheduler.add_job(send_gongfang_message, "cron", day_of_week="2,4", hour=19, minute=30,
                  args=["跨服·烂柯山 世界boss 将在20:00(分线20:05)进行。"])


def emm():
    pass

import re
from khl import *


class Manage:
    def __init__(self):
        self.version = "1.0.0"
        self.author = "迷路的茴香豆"

    def HookCreateCommand(self):
        # 创建指令列表，文本和定义的函数要对应上
        command = []
        return command

    def HookAdminCommand(self):
        # 管理员才能使用的指令
        adminCommand = ["t", "ban", ""]
        return adminCommand

    def HookCreateEvent(self):
        # 创建事件列表
        event = []
        return event

    # T人
    async def t(self, botObj: Bot, msgObj, msgArray):
        # 参数一：msg对象，参数二：分割好的数组，除掉指令，从下标从1开始为后续参数，参数三：tool助手类，
        if len(msgArray) >= 2:  # 说明接收到了2个以上参数
            for uid in msgObj.mention:
                await botObj.client.kickout(msgObj.guild.id, str(uid))
            await msgObj.reply("已经把@的人都赶走了")

    async def ban(self, botObj: Bot, msgObj: Message, msgArray):
        # 参数一：msg对象，参数二：分割好的数组，除掉指令，从下标从1开始为后续参数，参数三：tool助手类，
        if len(msgArray) >= 2:  # 说明接收到了2个以上参数
            for uid in msgObj.mention:
                await botObj.client.gate.request('POST', 'blacklist/create',
                                                 data={"guild_id": msgObj.guild.id, "target_id": str(uid)})
            await msgObj.reply("已经把@的人都拉黑了")

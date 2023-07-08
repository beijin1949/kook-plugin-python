import configparser
import json
import os


class Welcome:
    def __init__(self):
        self.version = "1.0.0"
        self.author = "迷路的茴香豆"
        self.config = configparser.ConfigParser()
        self.path = './Plugin/welcome/data/'  # 配置项路径
        # self.path = '/www/Python/kook_1/Plugin/welcome/data/'  # 配置项路径

    def HookCreateCommand(self):
        # 创建指令列表，文本和定义的函数要对应上
        command = []
        return command

    def HookAdminCommand(self):
        # 管理员才能使用的指令
        adminCommand = ["welcomeChanel", "welcomeType", "setWelcomeMsg"]
        return adminCommand

    def HookCreateEvent(self):
        # 创建事件列表
        event = ["JOINED_GUILD"]
        return event

    async def HookJoinGuildEvent(self, bot, event):
        # 加入服务器时触发
        absolute_path = os.path.abspath(self.path + event.target_id + ".ini")
        configFile = self.config.read(absolute_path)  # 读取配置文件
        if configFile:  # 路径下有文件的时候
            if not self.config['SET']['bindChannel'] == "":
                c = await bot.client.fetch_public_channel(self.config['SET']['bindChannel'])
                if self.config['SET']['cardTemp'] == "1": await c.send(
                    "(met)" + event.extra['body']['user_id'] + "(met) " + self.config['SET']['msg'])
                if self.config['SET']['cardTemp'] == "2":
                    # 卡片消息,这里用json代替，如有需要请用khl.card
                    user = await bot.client.fetch_user(event.extra['body']['user_id'])
                    CardTemp = '[{"type":"card","theme":"primary","size":"lg","modules":[{"type":"section","text":{"type":"kmarkdown","content":"**入群通知**"}},{"type":"section","text":{"type":"plain-text","content":"' + \
                               self.config['SET'][
                                   'msg'] + '"},"mode":"right","accessory":{"type":"image","src":"' + user.avatar + '","size":"sm"}}]}]'
                    await c.send(json.loads(CardTemp))

    # 绑定欢迎通知频道
    async def welcomeChanel(self,bot, msgObj, msgArray):
        # 参数一：msg对象，参数二，分割好的数组，除掉指令，从下标从1开始为后续参数
        channel = msgObj.channel.id  # 要绑定的频道
        absolute_path = os.path.abspath(self.path + msgObj.guild.id + ".ini")
        configFile = self.config.read(absolute_path)  # 读取配置文件
        if configFile:  # 路径下有文件的时候
            self.config['SET']['bindChannel'] = channel  # 直接改配置
        else:
            self.config['SET'] = {
                "bindChannel": channel,
                "cardTemp": "1",
                "msg": "欢迎加入我们"
            }  # 初始化配置
        with open(absolute_path, 'w') as config_file:
            self.config.write(config_file)  # 保存配置文件
        await msgObj.reply("绑定通知频道成功！")

    # 绑定欢迎语的模板
    async def welcomeType(self,bot, msgObj, msgArray):
        # 参数一：msg对象，参数二：分割好的数组，除掉指令，从下标从1开始为后续参数，参数三：tool助手类，
        if len(msgArray) == 2:  # 说明接收到了1个参数
            absolute_path = os.path.abspath(self.path + msgObj.guild.id + ".ini")
            configFile = self.config.read(absolute_path)  # 读取配置文件

            if msgArray[1] == "1":  # 如果第一个参数为 “0” 时处理的内容
                if configFile:  # 路径下有文件的时候
                    self.config['SET']['cardTemp'] = "1"  # 直接改配置
                else:
                    self.config['SET'] = {
                        "bindChannel": "",
                        "cardTemp": "1",
                        "msg": "欢迎加入我们"
                    }  # 初始化配置
            elif msgArray[1] == "2":
                if configFile:  # 路径下有文件的时候
                    self.config['SET']['cardTemp'] = "2"  # 直接改配置
                else:
                    self.config['SET'] = {
                        "bindChannel": "",
                        "cardTemp": "2",
                        "msg": "欢迎加入我们"
                    }  # 初始化配置

            with open(absolute_path, 'w') as config_file:
                self.config.write(config_file)  # 保存配置文件
            await msgObj.reply("修为消息模板成功")

    # 设置自定义欢迎语
    async def setWelcomeMsg(self,bot, msgObj, msgArray):
        # 参数一：msg对象，参数二，分割好的数组，除掉指令，从下标从1开始为后续参数
        if len(msgArray) == 2:  # 说明接收到了1个参数
            absolute_path = os.path.abspath(self.path + msgObj.guild.id + ".ini")
            configFile = self.config.read(absolute_path)  # 读取配置文件
            if configFile:  # 路径下有文件的时候
                self.config['SET']['msg'] = msgArray[1]  # 直接改配置
            else:
                self.config['SET'] = {
                    "bindChannel": "",
                    "cardTemp": "1",
                    "msg": msgArray[1]
                }  # 初始化配置

            with open(absolute_path, 'w') as config_file:
                self.config.write(config_file)  # 保存配置文件
            await msgObj.reply("修改配置文件成功！")

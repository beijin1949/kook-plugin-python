from core.core import Core
import json
from khl import *

with open('env.json', 'r', encoding='utf-8') as fp:
    ENV = json.load(fp)
# 根据开发环境自动切换配置
if ENV.dev:
    bot = Bot(token="1/MTA5Mzk=/U7bgcYWyDIz0Jlnypjp2Vw=="),
else:
    bot = Bot(cert=Cert(token=ENV.token, verify_token=ENV.verify_token, encrypt_key=ENV.encrypt_key), port=ENV.port)
# 初始化核心
Core = Core()


# 绑定机器人
@bot.command(name='bind')
async def bind_server(msg: Message, token: str = None):
    guild_id = msg.guild.id  # 服务器ID
    Guild = await bot.client.fetch_guild(guild_id)
    GuildUser = await bot.client.gate.request('GET', 'guild/user-list', params={"guild_id": guild_id})
    if token is None:
        await msg.reply("指令：/bind <密钥>\n绑定密钥不能为空！")
    res = await Core.bind_serve(token, guild_id, Guild.name, GuildUser['user_count'], msg.author.id,
                                msg.author.nickname, ENV.Bid)
    if res['code'] == 200:
        await msg.reply("绑定成功,请在控制端返回用户页面查看！")
    elif res['code'] == 2001:
        await msg.reply("密钥错误或已过期请重试")
    elif res['code'] == 3001:
        await msg.reply("该服务器已被其他账号绑定，请联系官方或者在线客服解绑操作")
    else:
        await msg.reply("未知错误，请联系官方！")


guild_config = {}
pluginObj = Core.load_plugin()
pluginKeyValue = Core.load_k_v(pluginObj)


@bot.on_message()
async def bot_msg(msg: Message):
    if msg.guild.id in guild_config:
        if Core.checkPrefix(msg.content[0], guild_config[msg.guild.id]["config"]['command_prefix']):
            # 检测到指令前缀
            serverCommandList = guild_config[msg.guild.id]['command_list']  # 读取所有的指令
            serverAdminCommandList = guild_config[msg.guild.id]['admin_command_list']  # 读取管理员指令
            commandStr = msg.content[1:].split(" ")  # 分割所有指令参数
            if commandStr[0] in serverCommandList:  # 如果指令在指令列表中
                pluginName = pluginKeyValue[commandStr[0]]  # 从键值对中读取指令所对应的插件名称
                s = await Core.send_power(pluginName, msg.guild.id)
                if s['code'] == 200:
                    strs = "pluginObj['" + pluginName + "']." + commandStr[0] + "(msg,commandStr)"
                    await eval(strs)
                elif s['code'] == 3100:
                    await msg.reply("没电了，没力气了，罢工！")
                else:
                    await msg.reply("插件异常")
            elif commandStr[0] in serverAdminCommandList:  # 如果指令在管理员指令列表中
                for ac in guild_config[msg.guild.id]["config"]['admin']:
                    if ac['id'] == msg.author_id:
                        pluginName = pluginKeyValue[commandStr[0]]  # 从键值对中读取指令所对应的插件名称
                        s = await Core.send_power(pluginName, msg.guild.id)
                        if s['code'] == 200:
                            strs = "pluginObj['" + pluginName + "']." + commandStr[0] + "(bot,msg,commandStr)"
                            await eval(strs)
                        elif s['code'] == 3100:
                            await msg.reply("没电了，没力气了，罢工！")
                        else:
                            await msg.reply("插件异常")
                    else:
                        await msg.reply("你不是管理员，不能使用管理员指令~")
    else:
        res = await Core.get_server_config(msg.guild.id)
        if res['code'] == 200:
            commandList = []  # 指令列表
            adminCommandList = []  # 管理员指令列表
            eventList = {}  # 事件列表
            if res['data']['plugin_list'] is not None:
                plugin_item = json.loads(res['data']['plugin_list'])  # 读取所有的插件列表
                for pi in plugin_item:
                    commandList.extend(pluginObj[pi].HookCreateCommand())  # 读取所有有效指令
                    adminCommandList.extend(pluginObj[pi].HookAdminCommand())  # 读取管理员列表
                    for hook in pluginObj[pi].HookCreateEvent():  # 插件所有钩子
                        if hook in eventList:
                            eventList[hook].insert(pi)
                        else:
                            eventList[hook] = [pi]
                config = json.loads(res['data']['config'])  # 加载指令前缀配置
                guild_config[msg.guild.id] = {"config": config, "command_list": commandList,
                                              "admin_command_list": adminCommandList, "event_list": eventList}
                await msg.reply("ヾ(≧▽≦*)o不好意思溜神了,请再发一遍指令吧~")
                Core.logger_info(msg.guild.id + "首次激活")
        elif res['code'] == 3000:
            await msg.reply(
                "该服务器未在用户端配置，请前往微信小程序【kook机器人】激活，如果无需使用请从服务器移出本机器人")
            Core.logger_error(msg.guild.id + "服务器未激活")


@bot.on_event(EventTypes.JOINED_GUILD)
async def bot_event(bot, event):
    if event.target_id in guild_config:  # 机器人开启了
        if "JOINED_GUILD" in guild_config[event.target_id]["event_list"]:
            for i in guild_config[event.target_id]['event_list']['JOINED_GUILD']:
                str = "pluginObj['" + i + "'].HookJoinGuildEvent(bot,event)"
                await eval(str)


bot.run()

import aiohttp
from core.color_log import Logger

from Plugin.welcome.main import Welcome
from Plugin.manage.main import Manage


class Core:
    def __init__(self):
        self.apiUrl = "https://kookbot.app.fishwo.com/api/"
        self.Authorization = "9CD8A2455B1839FF98EF70C05B9B5983"
        self.logger = Logger(name="log")

    async def api(self, url, body={}):
        async with aiohttp.request(url=self.apiUrl + url, data=body, headers={"Authorization": self.Authorization},
                                   method="POST") as res:
            return await res.json()

    async def bind_serve(self, token, guild_id, guild_name, people_num, uid, uname, BOTID):
        return await self.api(url="bot/bindServer",
                              body={"key": token, "name": guild_name, "gid": guild_id, "num": people_num, 'kid': uid,
                                    'kname': uname, 'bid': BOTID})

    async def get_server_config(self, guild_id):
        return await self.api(url="index/getServerConfig", body={"sid": guild_id})

    async def send_power(self, plugin, gid):
        return await self.api(url="bot/powerRemove", body={"pid": plugin, 'gid': gid})

    def load_plugin(self):
        self.logger.info(" 加载插件中...")
        # 加载插件开始
        # ---------------------
        initObj = {
            "welcome": Welcome(),
            "manage": Manage()
        }
        self.logger.info(" 插件加载成功")
        return initObj

    def load_k_v(self, pluginList):
        d = {}
        for k, v in pluginList.items():
            for item in v.HookCreateCommand():
                d[item] = k
            for item in v.HookAdminCommand():
                d[item] = k
        return d

    def logger_error(self, msg):
        self.logger.error(" " + msg)

    def logger_info(self, msg):
        self.logger.info(" " + msg)

    def checkPrefix(self, msg_first, gc):
        if gc == "0": z = "/"
        if gc == "1": z = "."
        if gc == "3": z = "~"

        if z == msg_first:
            return True
        else:
            return False

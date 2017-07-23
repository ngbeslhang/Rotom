import discord
from discord.ext import commands
from ruamel import yaml

class MsgBlock:
    def __init__(self, bot, conf):
        self.bot = bot
        self.config = conf

    @commands.group(aliases=["adblock"])
    async def msgblock(self, ctx):
        pass

    async def on_message(self, msg):
        try:
            await self.bot.db.write("server", {"id": msg.server.id}, conflict="error")
        except RuntimeError:
            svr_dat = await self.bot.db.select("server", msg.server.id)
        except ConnectionError:
            self.bot.log.error("[MsgBlock Unable to connect to database!]")
            return

        # await get_invite(url)

    def _conf_parse(self, ctx, conf: dict):
        """Parse the config then saves it into the database."""

def setup(bot):
    try:
        # Possible URL regex:
        # (?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z¡-￿0-9]-?)*[a-z¡-￿0-9]+)(?:\.(?:[a-z¡-￿0-9]-?)*[a-z¡-￿0-9]+)*(?:\.(?:[a-z¡-￿]{2,})))(?::\d{2,5})?(?:/\S*)?
        # Credits to adamrofer @ https://gist.github.com/dperini/729294
        conf = bot.get_conf()
        bot.add_cog(MsgBlock(bot, conf))
    except:
        bot.log.error("quak")

from ruamel import yaml
from discord.ext.commands import command

import re

class Tags:
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def get(self, *, query):
        pass

def setup(bot):
    bot.add_cog(Tags(bot))
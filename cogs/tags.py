from ruamel import yaml
from discord.ext.commands import command

class Tags:
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Tags(bot))
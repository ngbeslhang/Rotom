import discord
from discord.ext import command
from ruamel import yaml

class MsgBlock:
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(MsgBlock(bot))
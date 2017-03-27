"""Admin cog for Rotom"""
from discord.ext import commands
from utils import checks

class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["hammer"], pass_context=True)
    @checks.is_admin()
    async def ban(self, ctx):
        pass
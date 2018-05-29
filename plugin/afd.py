import textwrap
import traceback
from discord.ext import commands
import discord
import io
from contextlib import redirect_stdout

# Properly crediting the author
__title__ = "rotom-rpkmn_afd"
__author__ = "Kaihang Eng"
__copyright__ = "Copyright 2018 Kaihang Eng"

class AFD:
    def __init__(self, bot):
        self.bot = bot
        self.enabled = False
        self.gibrole = ['it doesn\'t exist', 'it does not exist']
        self.jellyworld = ['jellyworld', 'jelly world', '<#426400788626014239>']

    @commands.command(hidden=True)
    async def afd_start(self, ctx):
        if ctx.author.id in [111682132115509248, 129977953034567681]:
            self.enabled = True
            await ctx.send("AFD Enabled!")

    @commands.command(hidden=True)
    async def afd_end(self, ctx):
        if ctx.author.id in [111682132115509248, 129977953034567681]:
            self.enabled = False
            await ctx.send("AFD Disabled!")

    async def on_message(self, msg):
        if self.enabled and msg.guild.id == 111504456838819840:
            role = discord.utils.find(lambda r: r.id == 426422214502645760, msg.guild.roles)
            has_role = any(a for a in msg.author.roles if a is role)
            em = discord.Embed(colour=discord.Colour.green())

            if any(x in msg.content.lower() for x in self.gibrole) and not has_role:
                await msg.author.add_roles(role,
                                       reason="[AFD] Welcome to the club.")
                em.title = "WELCOME TO THE CLUB"
                await self.send_embed(msg, em)
            elif any(x in msg.content.lower() for x in self.jellyworld) and has_role:
                await msg.author.remove_roles(role,
                                          reason="[AFD] It does not exist.")
                em.title = "No, it doesn't exist"
                await self.send_embed(msg, em)

    async def send_embed(self, msg, em):
        if msg.author.avatar_url is not None:
            em.set_author(name=str(msg.author), icon_url=msg.author.avatar_url)
        else:
            em.set_author(name=str(msg.author), icon_url=msg.author.default_avatar_url)

        em.add_field(name="Content", value=msg.content, inline=False)
        em.add_field(name="User ID", value=msg.author.id)
        em.add_field(name="Message ID", value=msg.id)
        em.add_field(name="Posted at", value=msg.channel.name)

        await self.bot.get_channel(328507346655641601).send(embed=em)

def setup(bot):
    bot.add_cog(AFD(bot))
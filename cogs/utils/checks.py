"""Some of them shamelessly copied from RoboDanny :Thonkang:"""
from discord.ext import commands

def is_owner_check(ctx):
    return ctx.message.author.id in (ctx.bot.owner, ctx.bot.user.id)

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx))
"""Some of them shamelessly copied from RoboDanny :Thonkang:"""
from discord.ext import commands

def is_owner_check(msg, owner):
    return msg.author.id in owner

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message, ctx.bot.owner))
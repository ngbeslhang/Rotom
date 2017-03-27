"""Some of them shamelessly copied from RoboDanny :Thonkang:"""
from discord.ext import commands


# Owner check
def is_owner_check(ctx):
    return ctx.message.author.id in (ctx.bot.owner, ctx.bot.user.id)

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx))


# Superuser check
def is_superuser_check(ctx):
    # Always true no matter what, that way database also don't need to record server owner's ID
    if ctx.message.author.id in (ctx.message.server.owner.id, *ctx.bot.owner):
        return True

    if ctx.bot.db is None:
        return (ctx.bot.defaults['superuser'] is not None and 
                ctx.bot.defaults['superuser'].lower() in [a.name.lower() for a in ctx.message.author.roles])
    else:
        # We'll get to this later
        pass

def is_superuser():
    return commands.check(lambda ctx: is_superuser_check(ctx))


# Admin check
def is_admin_check(ctx):
    # Always true no matter what, that way database also don't need to record server owner's ID
    if ctx.message.author.id is ctx.message.server.owner.id:
        return True

    if ctx.bot.db is None:
        return (ctx.bot.defaults['admin'] is not None and 
                ctx.bot.defaults['admin'].lower() in [a.name.lower() for a in ctx.message.author.roles])
    else:
        # We'll get to this later
        pass

def is_admin():
    return commands.check(lambda ctx: is_admin_check(ctx))
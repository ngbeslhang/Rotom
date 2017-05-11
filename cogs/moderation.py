from discord.ext import commands
from ruamel import yaml


# Command checks
def is_admin(ctx):
    # Get default role names from ctx.bot
    # Get specified role IDs in ctx.bot.db

    # If not, check if said user have administrator perm
    permissions = ctx.message.channel.permission_for(ctx.message.author)
    admin_perm = {"administrator": True}
    return all(getattr(permissions, perm, None) == value for perm, value in admin_perm.items())
    pass

# Refer http://discordpy.readthedocs.io/en/rewrite/api.html#discord.Permissions
def is_mod(**perms):
    # Get default role names from ctx.bot
    # Get specified role IDs in ctx.bot.db
    def predicate(ctx):
        pass
        # If not, check if said user have specied perm
    return commands.check(predicate)


class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["mod"])
    @commands.guild_only()
    @commands.check(is_admin)
    async def modsettings(self, *, settings):
        pass


def setup(bot):
    bot.add_cog(Moderation(bot))
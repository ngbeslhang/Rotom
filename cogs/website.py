"""Website cog for Rotom written in aiohttp.

This file only contains the necessary cog class and setup() function for discord.py command extension.
For the main code, visit the cog_website folder."""

from .cog_website import Site

class Website:
    def __init__(self, bot):
        try:
            bot.loop.run_until_complete(Site().start())
        except OSError:
            bot.log.error("[Website] Unable to start server with provided settings!")


def setup(bot):
    bot.add_cog(Website(bot))

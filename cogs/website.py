"""Website cog for Rotom written in Kyoukai and Asphalt.

This file only contains the necessary cog class and setup() function for discord.py command extension.
For the main code, visit the cog_website folder."""

from .cog_website import app

class Website:
    def __init__(self, bot):
        bot.loop.create_task(app.run())


def setup(bot):
    bot.add_cog(Website(bot))
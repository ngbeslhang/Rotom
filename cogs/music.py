"""Music feature for Rotom"""
#import discord
from discord.ext.commands import command

class Music:
    """
    Music cog for Rotom
    **NOTE**: Must be modified to be compactible with other discord.ext bots.
    Rotom-exclusive parts:
    - Database"""
    def __init__(self, bot):
        self.bot = bot
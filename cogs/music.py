"""Music feature for Rotom"""
import asyncio
#import discord
from discord.ext.commands import command


class MusicEntry:
    """Music entry class for Queue class"""
    def __init__(self, player, mode):
        """Initialize with player and mode.

        player    - discord.py's built-in player coroutine
                    If the URL provided is a playlist, a list of players instead.
                    Considering setting a limit per playlist
                    The skip command, if used without "playlist" or "pl" or "list",
                    only skips to the next player in the list, otherwise the whole playlist
                    will be skipped instead.
        mode: str - Player mode, e.g. yt, sc, twitch
        """
        self.player = player
        self.mode = mode

class Queue:
    """Queue class for _queue"""
    def __init__(self, text_channel):
        """
        """
        self.text_channel = text_channel
        #self._queue = 

class Music:
    """
    Music cog for Rotom
    **NOTE**: Must be modified to be compactible with other discord.ext bots.
    Rotom-exclusive parts:
    - Database"""

    def __init__(self, bot):
        self.bot = bot
        self._queue = {}
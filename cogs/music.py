"""Music feature for Rotom"""
#import functools
import asyncio
#import discord
#import youtube_dl
from discord.ext.commands import command


class MusicEntry:
    """Music entry class for Server._queue class"""

    def __init__(self, player, service, requester):
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
        self.service = service
        self.requester = requester


class Server:
    """Server class for _servers"""

    def __init__(self, text_channel):
        """text_channel - Text channel's ID"""
        self.text_channel = text_channel
        self._queue = asyncio.Queue()  # for now


class Music:
    """
    Music cog for Rotom
    **NOTE**: Must be modified to be compactible with other discord.ext bots.
    Rotom-exclusive parts:
    - Database"""

    def __init__(self, bot):
        self.bot = bot
        self._servers = {}

    @command(aliases=['add'], pass_context=True)
    async def play(self, ctx, *, query: str):
        """Check the query and pass it to player accordingly."""
        try:
            if self.bot.voice_client_in():
                client = self.bot.voice_client_in(ctx.message.server)
            else:
                if ctx.message.author.voice.voice_channel != None:
                    self.bot.say(
                        "The bot isn't on any voice channel on this server! " \
                        "Attempting to connect to the voice channel you are in...")
                    client = yield from self.bot.join_voice_channel(
                        ctx.message.author.voice.voice_channel)
                    self.bot.say("Connected to voice channel `{}`.".format(
                        ctx.message.author.voice.voice_channel.name))
                else:
                    self.bot.say(
                        "Please join a voice channel before using this command."
                    )
            opt = {'default-search': 'ytsearch'}
            s = 'YouTube'
            queue = self._servers[ctx.message.server.id]._queue
        except KeyError:
            self._servers[ctx.message.server.id] = Server(ctx.message.channel)
            queue = self._servers[ctx.message.server.id]._queue
            self.bot.say("Binded to text channel {}.".format(
                ctx.message.channel.mention))

        # Need to find a way to shorten this mess
        if query[:3].lower() is "yt:":
            q = query[3:]
        elif query[:8].lower() is "youtube:":
            q = query[8:]
        elif query[:3].lower() is "sc:":
            opt['default-search'] = 'scsearch'
            s = 'SoundCloud'
            q = query[3:]
        elif query[:11].lower() is "soundcloud:":
            opt['default-search'] = 'scsearch'
            s = 'SoundCloud'
            q = query[11:]
        elif query[:2].lower() is "t:":
            q = 'https://twitch.tv/' + query[2:]
            s = 'Twitch'
        elif query[:7].lower() is "twitch:":
            q = 'https://twitch.tv/' + query[7:]
            s = 'Twitch'
        else:
            q = query[:]

        player = yield from client.create_ytdl_player(q, ytdl_options=opt)
        queue.append(MusicEntry(player, s, ctx.message.author))

    '''
    async def _create_player(self, query, client, *, ytdl_options=None, **kwargs):
        """Creates a player, partially based on discord.VoiceClient.create_ytdl_player
        
        query: str
        client: discord.VoiceClient
        """
        use_avconv = kwargs.get('use_avconv', False)
        opts = {
            'format': 'bestaudio',
            'prefer_ffmpeg': not use_avconv
        }

        if ytdl_options is not None and isinstance(ytdl_options, dict):
            opts.update(ytdl_options)

        # Check the query, set default-search to YT by default or other services
        # by default if indicator was given.

        ydl = youtube_dl.YoutubeDL(opts)
        try:
            pass
        except youtube_dl.utils.ExtractorError:
            opts.update()
    '''


def setup(bot):
    bot.add_cog(Music(bot))
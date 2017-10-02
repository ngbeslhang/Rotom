"""Rotom's core"""
import sys
import inspect
import importlib
import asyncio
import discord

class Bot(discord.ext.commands.AutoShardedBot):
    def __init__(self, **kwargs):
        # Initializations
        import time
        self.boot_time = time.time()

    def _init_log(self, conf_name, debug):
        """Initialize logging."""
        import datetime, os, logging
        # Credits to Liara: https://github.com/Thessia/Liara/blob/master/liara.py#L83
        now = str(datetime.datetime.now()).replace(' ', '_').replace(':', '-').split('.')[0]
        formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(message)s', datefmt='GMT%z %Y-%m-%d %I:%M:%S %p')

        self.log = logging.getLogger('rotom')
        if debug:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)

        # Creates a log folder if it doesn't exist just in case
        if not os.path.exists("logs/"):
            os.makedirs("logs/")

        if not os.path.exists("logs/rotom"):
            os.makedirs("logs/rotom")

        handler = logging.FileHandler('logs/rotom/rotom-{}_{}.log'.format(conf_name, now))
        handler.setFormatter(formatter)
        self.log.addHandler(handler)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.info("Successfully set up logging!")

        self.discord_log = logging.getLogger('discord')
        self.discord_log.setLevel(logging.INFO)

        if not os.path.exists("logs/discord"):
            os.makedirs("logs/discord")

        handler = logging.FileHandler('logs/discord/discord-{}_{}.log'.format(config, now))
        handler.setFormatter(formatter)
        self.discord_log.addHandler(handler)
        self.log.info("Successfully set up discord.py logging!")

    async def on_bot_init(self):
        """Special event for listeners at bot initialization"""
        pass

    def add_cog(self, cog):
        """Modified the original add_cog() for dependancy support.

        Parameters
        ----------
        cog
            The cog to register to the bot.
        """
        # TODO: Add dependancy support
        self.cogs[type(cog).__name__] = cog

        try:
            check = getattr(cog, '_{.__class__.__name__}__global_check'.format(cog))
        except AttributeError:
            pass
        else:
            self.add_check(check)

        try:
            check = getattr(cog, '_{.__class__.__name__}__global_check_once'.format(cog))
        except AttributeError:
            pass
        else:
            self.add_check(check, call_once=True)

        members = inspect.getmembers(cog)
        for name, member in members:
            # register commands the cog has
            if isinstance(member, Command):
                if member.parent is None:
                    self.add_command(member)
                continue

            # register event listeners the cog has
            if name.startswith('on_'):
                self.add_listener(member, name)


    def load_estension(self, name):
        """Loads an extension.
        An extension is a python module that contains commands, cogs, or
        listeners.
        An extension must have a global function, ``setup`` defined as
        the entry point on what to do when the extension is loaded. This entry
        point must have a single argument, the ``bot``.
        Parameters
        ------------
        name: str
            The extension name to load. It must be dot separated like
            regular Python imports if accessing a sub-module. e.g.
            ``foo.test`` if you want to import ``foo/test.py``.
        Raises
        --------
        ClientException
            The extension does not have a setup function.
        ImportError
            The extension could not be imported.
        """

        if name in self.extensions:
            return

        lib = importlib.import_module(name)
        if not hasattr(lib, 'setup'):
            del lib
            del sys.modules[name]
            raise discord.ClientException('extension does not have a setup function')

        lib.setup(self)
        self.extensions[name] = lib
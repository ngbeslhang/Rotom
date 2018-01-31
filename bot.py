"""Rotom's core"""
import os
import sys
import inspect
import importlib
import asyncio
import discord
from discord.ext import commands
from ruamel import yaml

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        # Initializations
        import time
        self.boot_time = time.time()
        config = kwargs.pop('config', 'config.yml')
        debug = kwargs.pop('debug', False)
        self._init_log(config, debug)

        # Loading config file
        try:
            with open(config) as c:
                conf = yaml.safe_load(c)
                self.log.info("Successfully loaded config file {}!".format(config))
        except FileNotFoundError:
            self.log.error("Unable to find {}".format(config))
            sys.exit(2)

        # Changes CWD to parent dir of Rotom's main script for plugin loading
        #self.log.info(os.path.dirname(__file__))

        # superinit commands.Bot with params
        params = conf['bot']['params']
        if params is None:
            params = {}

        prefix = conf['bot']['prefix']
        if isinstance(prefix, str):
            prefix = [prefix] if isinstance(prefix, str) else prefix
        params.update({
            "command_prefix": self.when_mentioned_or(*prefix)
        })

        super().__init__(**params)
        self.log.info("Successfully initialized the bot with provided params!")

        # Load plugins
        import traceback

        plugin_conf = conf['bot']['plugins']
        plugins = plugin_conf['load']

        if isinstance(plugin_conf['load'], (list, str)):
            plugins = [plugins] if isinstance(plugins, str) else plugins
            # Actually loading plugins
            for p in plugins:
                try:
                    self.load_extension('plugins.'+p)
                    self.log.info('Successfully imported plugin {}!'.format(p))
                except:
                    self.log.error("Unable to import module {}!".format(p))
                    self.log.error(traceback.format_exc())
        else:
            self.log.info('No plugins to load at initialization.')

        # For self.start()
        self.token = conf['bot']['token']
        self.is_bot = not params.pop('self_bot', False)

    def _init_log(self, conf_name, debug):
        """Initialize logging."""
        import datetime, logging
        # Credits to Liara: https://github.com/Thessia/Liara/blob/master/liara.py#L83
        now = str(datetime.datetime.now()).replace(' ', '_').replace(':', '-').split('.')[0]
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)s: %(message)s', datefmt='GMT%z %Y-%m-%d %I:%M:%S %p')

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

        handler = logging.FileHandler('logs/discord/discord-{}_{}.log'.format(conf_name, now))
        handler.setFormatter(formatter)
        self.discord_log.addHandler(handler)
        self.log.info("Successfully set up discord.py logging!")

    def when_mentioned_or(self, *prefixes):
        """Modified discord.ext.commands.when_mentioned_or for custom per-server prefixes checking.

        Added a fix for a bug that process_command() will only use the first matching prefix, thus
        if someone uses different-length same-char prefixes in order of shortest length the longer
        will be considered a CommandNotFound error.

        e.g. [':', '::'] as prefix, process_command only match `::help` with prefix ':', thus the
        bot will return error regarding `:help` not being a command."""

        def inner(bot, msg):
            r = list(prefixes)
            r.append(commands.when_mentioned(bot, msg))

            # Check if there's custom prefix
            # try:
            #     if self.db is not None:
            #         pass
            # except AttributeError:
            #     pass
            # If custom prefix is not None:
            # r.append(list(custom_prefix_list))
            r = sorted(r, key=len, reverse=True)
            return r

        return inner

    async def on_bot_init(self):
        """Special event for listeners at bot initialization"""
        pass

    async def on_ready(self):
        self.log.info("The bot is now ready for use!")

    # Everything below are modified functions inside discord.Client/command.Bot

    def run(self, **kwargs):
        """Starts the bot. Source code based on discord.py's Client.run().

        WARNING: This function is blocking, read discord.Client.run.__doc__ for details."""
        import signal
        from discord import compat

        is_windows = sys.platform == 'win32'
        loop = self.loop
        if not is_windows:
            loop.add_signal_handler(signal.SIGINT, self._do_cleanup)
            loop.add_signal_handler(signal.SIGTERM, self._do_cleanup)

        task = compat.create_task(self.start(**kwargs), loop=loop)

        def stop_loop_on_finish(fut):
            loop.stop()

        task.add_done_callback(stop_loop_on_finish)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            self.discord_log.info('Received signal to terminate bot and event loop.')
        finally:
            task.remove_done_callback(stop_loop_on_finish)
            if is_windows:
                self._do_cleanup()

            loop.close()
            if task.cancelled() or not task.done():
                return None
            return task.result()

    async def start(self, **kwargs):
        """Starts the bot in an asynchronous way"""
        bot = kwargs.pop('bot', self.is_bot)
        del self.is_bot
        #reconnect = kwargs.pop('reconnect', True)
        await self.login(self.token, bot=bot)
        del self.token
        await self.connect()

    def _do_cleanup(self):
        self.discord_log.info('Cleaning up event loop.')
        loop = self.loop
        if loop.is_closed():
            return # we're already cleaning up

        task = discord.compat.create_task(self.close(), loop=loop)

        def _silence_gathered(fut):
            try:
                fut.result()
            except:
                pass
            finally:
                loop.stop()

        def when_future_is_done(fut):
            pending = asyncio.Task.all_tasks(loop=loop)
            if pending:
                self.discord_log.info('Cleaning up after %s tasks', len(pending))
                gathered = asyncio.gather(*pending, loop=loop)
                gathered.cancel()
                gathered.add_done_callback(_silence_gathered)
            else:
                loop.stop()

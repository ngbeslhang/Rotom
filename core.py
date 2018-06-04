# -*- coding: utf-8 -*-
"""Rotom Core

This program is licensed under MIT license, for more details see LICENSE file. 
"""

__title__ = "rotom-core"
__author__ = "Kaihang Eng"
__copyright__ = "Copyright 2016-2018 Kaihang Eng"

__license__ = "MIT"
__version__ = '0.1.0'
__status__ = "Development"

import sys
import os
import asyncio
import discord
from discord.ext import commands
from ruamel import yaml

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        """Setting up the bot."""
        # Version check for plugins
        global __version__
        self.__version__ = __version__

        import time
        self.boot_time = time.time()
        config = kwargs.pop('config', 'config.yml')
        debug = kwargs.pop('debug', False)
        self._init_log(config, debug)
        self._db = None # For database plugins

        # Load config file
        try:
            with open(config) as c:
                conf = yaml.safe_load(c)
                self.log.info(f"Successfully loaded config file {config}!")
        except FileNotFoundError:
            self.log.error(f"Unable to find config file {config}!")
            sys.exit(2)
        
        # Saves the token as a variable for start() and to show the config via debug logs
        self.token = conf['bot']['token']
        conf['bot']['token'] = '***'
        self.log.debug(f"Loaded config file:")

        # Loads plugin files
        # If file starts with "db_" and if it's successfully imported, ignore absolutely anything else that starts with "db_"

        # superinit commands.AutoShardedBot with params
        params = conf['bot']['params']
        if params is None:
            params = {}
        self.is_bot = not params.pop('self_bot', False)

    def _init_log(self, conf_name, debug):
        """Initialize logging."""
        import datetime, logging
        # Credits to Liara: https://github.com/Thessia/Liara/blob/master/liara.py#L83
        now = str(datetime.datetime.now()).replace(' ', '_').replace(':', '-').split('.')[0]

        self.log = logging.getLogger('rotom')
        self.discord_log = logging.getLogger('discord')

        if debug:
            self.log.setLevel(logging.DEBUG)
            self.discord_log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)
            self.discord_log.setLevel(logging.INFO)

        # Creates a log folder if it doesn't exist just in case
        if not os.path.exists("logs/"):
            os.makedirs("logs/")

        handler = logging.FileHandler('logs/rotom-{}_{}.log'.format(conf_name, now))
        con_handler = logging.StreamHandler(sys.stdout)

        # Set up logger
        formatter = logging.Formatter(
            fmt='[%(name)s] %(asctime)s.%(msecs)03d | %(levelname)s: %(message)s', datefmt='%Y-%m-%d %z %H:%M:%S')

        handler.setFormatter(formatter)
        con_handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.addHandler(con_handler)
        self.discord_log.addHandler(handler)
        self.discord_log.addHandler(con_handler)

        self.log.info("Successfully set up logging!")

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
        
    async def db(self, str: str):
        """Parse database requests.
        """

    # Everything below are modified functions inside discord.Client

    def run(self, **kwargs):
        """Starts the bot.
        WARNING: This function is blocking, read discord.Client.run.__doc__ for details."""
        import signal

        is_windows = sys.platform == 'win32'
        loop = self.loop
        if not is_windows:
            loop.add_signal_handler(signal.SIGINT, self._do_cleanup)
            loop.add_signal_handler(signal.SIGTERM, self._do_cleanup)

        task = discord.compat.create_task(self.start(**kwargs), loop=loop)

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
        """Starts the bot in an asynchronous way."""
        bot = kwargs.pop('bot', self.is_bot)
        del self.is_bot
        #reconnect = kwargs.pop('reconnect', True)
        await self.login(self.token, bot=bot)
        del self.token
        try:
            await self.connect()
        except discord.LoginFailure:
            self.discord_log.critical("Unable to log in, please double-check the token provided.")

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

        task.add_done_callback(when_future_is_done)
        if not loop.is_running():
            loop.run_forever()
        else:
            return None

        try:
            return task.result() # suppress unused task warning
        except:
            return None
        
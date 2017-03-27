"""Rotom's core"""
import sys
import os
import inspect
import time
import argparse
import logging
import datetime
import yaml

import discord
from discord.ext import commands

from cogs.utils import checks


class Bot(commands.Bot):
    """Bot class of Rotom derived from discord.ext.commands.Bot
    
    NOTE: It's NOT written with ability to derive in mind (reading discord.Client args from config file)."""

    def __init__(self, config, debug):
        """Initialize Rotom.

        config : str  - Config file name.
        debug  : bool - Debug mode, pass `True` to enable, `False` otherwise."""
        self.boot_time = time.time()

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

        handler = logging.FileHandler('logs/rotom_{}.log'.format(now))
        handler.setFormatter(formatter)
        self.log.addHandler(handler)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.info("Successfully set up logging")

        self.discord_log = logging.getLogger('discord')
        self.discord_log.setLevel(logging.INFO)

        handler = logging.FileHandler('logs/discord_{}.log'.format(now))
        handler.setFormatter(formatter)
        self.discord_log.addHandler(handler)
        self.log.info("Successfully set up discord.py logging")

        del handler, formatter, now

        # Loading config file
        try:
            with open(config) as c:
                conf = yaml.load(c)
                self.log.info("Successfully loaded config file {}".format(config))
        except FileNotFoundError:
            self.log.error("Unable to find {}".format(config))
            sys.exit(2)

        # using list() instead of tuple() allows anyone who have access to exec command to modify it.
        # + Can dynamically add owners w/o needing to restart the bot
        # - Can lock owners out of access or other malicious intents if the exec command was used improperly
        # But for security issues let's just use tuple()
        self.owner = tuple(conf['bot']['owner'])
        self.allow_bot = conf['bot']['allow_bot']
        self.defaults = conf['defaults']
        self.ready = False

        try:
            self.is_bot = not conf['params']['self_bot']
        except KeyError:
            self.is_bot = True

        if conf['bot']['db'] is None:
            self.db = None
        else:
            pass
            # search for db module with db_<name>.py as name in cogs then import it as command.Bot extension
            # otherwise, if not found set self.db as None

        # Unpacking config file's args
        params = conf['params']
        if params is None:
            params = {}

        # Updating params with other params
        params.update({"command_prefix": self.when_mentioned_or(*conf['bot']['prefix'])})

        super().__init__(**params)
        self.log.info("Initialized commands.Bot with config params.")

        # Loading builtins
        self.add_cog(Builtin(self))
        self.log.info("Successfully loaded builtin command cog.")

        self.log.info("Logging in using the provided token.")
        self.run(conf['bot']['token'], bot=self.is_bot)

    def when_mentioned_or(self, *prefixes):
        """Basically the same as discord.ext.commands.when_mentioned_or except it also checks for custom per-server prefixes via database."""

        def inner(bot, msg):
            r = []

            # Just in case PyYAML converts digit-only etc prefixes into numbers, all of them will be appended as str
            for a in prefixes:
                r.append(str(a))

            r.append(commands.when_mentioned(bot, msg))

            # Check if there's custom prefix
            if self.db is not None:
                pass
            # If custom prefix is not None:
            # r.append(list(custom_prefix_list))
            return r

        return inner

    # Command checks (Some based on RoboDanny)
    # def is_owner_check()

    def get_api_conf(self):
        """Gets config from API by searching matching config using caller module's name.
        
        If unable to find matching config, `None` will be returned instead."""
        conf = None

        with open(os.path.join(os.path.dirname(__file__), ''), 'r') as c:
            conf = yaml.load(c)

        # http://stackoverflow.com/questions/1095543/get-name-of-calling-functions-module-in-python
        # Can also be used on get_lang()
        frm = inspect.stack()[1]
        module = inspect.getmodule(frm[0]).__name__

        if module.startswith('db_') or module.startswith('api_'):
            return conf[module.split('_')[1]]
        else:
            return conf[module]

    # load_lang(), reload_lang() (could be set to be alias of load_lang() OR only reload modified files)
    # both should be similar as get_api_conf()
    def _say(self, lang: str="", *args, **kwargs):
        """Modified discord.ext.commands.bot.say() for localization support.
        
        If unable to find matching string, the key (aka default language) will be returned instead."""
        conf = None

        with open(os.path.join(os.path.dirname(__file__), ''), 'r') as c:
            conf = yaml.load(c)

        # http://stackoverflow.com/questions/1095543/get-name-of-calling-functions-module-in-python
        # Can also be used on get_lang()
        frm = inspect.stack()[1]
        module = inspect.getmodule(frm[0]).__name__

        if module.startswith('db_') or module.startswith('api_'):
            return conf[module.split('_')[1]]
        else:
            return conf[module]

    # Events
    async def on_ready(self):
        self.log.info("The bot is now ready to accept commands.")
        self.ready = True

    async def on_message(self, msg):
        if msg.author.bot:
            if not self.allow_bot:
                return

        if self.ready:
            #self.log.info("{0.content}".format(msg))
            await self.process_commands(msg)


class Builtin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True, aliases=['eval'])
    @checks.is_owner()
    async def debug(self, ctx, *, code: str):
        """Evaluates code, shamelessly copied from Robo Danny."""
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.message.server,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }

        env.update(globals())

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
            # Should we include channel in the log?
            self.log.info(
                "[EVAL] {0.author.name} ({0.author.id}) ran `{1}` in {0.server.name} ({0.server.id}).".
                format(ctx.message, code))
        except Exception as e:
            await self.bot.say(python.format(type(e).__name__ + ': ' + str(e)))

            self.log.info(
                "[EVAL] {0.author.name} ({0.author.id}) tried to run `{1}` in {0.server.name} ({0.server.id}) but was met with `{2}: {3}`.".
                format(ctx.message, code, type(e).__name__, str(e)))

            return

        await self.bot.say(python.format(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs Rotom.')
    parser.add_argument('-c', '--config', type=str, help='Config file name (default: config.yml)')
    parser.add_argument('-d', '--debug', help='Enable debug mode', action='store_true')
    args = parser.parse_args()
    if args.config is None:
        args.config = 'config.yml'
    rotom = Bot(config=args.config, debug=args.debug)

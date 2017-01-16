"""Rotom's core"""
import sys
import os
import time
import argparse
import logging
import datetime
import yaml

import discord
from discord.ext import commands

import rethinkdb
from rethinkdb.errors import ReqlDriverError, ReqlRuntimeError


class Bot(commands.Bot):
    """Bot class of Rotom derived from discord.ext.commands.Bot"""

    def __init__(self, config, debug):
        """Initialize Rotom.
        
        config : str  - Config file name.
        debug  : bool - Debug mode, pass `True` to enable, `False` otherwise."""
        self.boot_time = time.time()

        # Credits to Liara: https://github.com/Thessia/Liara/blob/master/liara.py#L83
        now = str(datetime.datetime.now()).replace(' ', '_').replace(':', '-').split('.')[0]
        formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='GMT%z %Y-%m-%d %I:%M:%S%p')

        self.log = logging.getLogger('rotom')
        if debug:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)

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

        try:
            with open(config) as c:
                conf = yaml.load(c)
                self.log.info("Successfully loaded config file {}".format(config))
        except FileNotFoundError:
            self.log.error("Unable to find {}".format(config))
            sys.exit(1)
        
        # Unpacking config file's args
        super().__init__(**conf['params'])
        self.run(conf['bot']['token'])


class Language:
    """Class for coglang"""

    def __init__(self):
        pass


class Builtin:
    """Builtin commands cog"""

    def __init__(self, bot):
        self.bot = bot


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs Rotom.')
    parser.add_argument('-c', '--config', type=str, help='Config file name (default: config.yml)')
    parser.add_argument('-d', '--debug', help='Enable debug mode', action='store_true')
    args = parser.parse_args()
    if args.config == None:
        args.config = 'config.yml'
    rotom = Bot(config=args.config, debug=args.debug)

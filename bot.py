"""Rotom's bot core"""
import os
import sys
#import asyncio
import logging
import yaml

import discord
from discord.ext import commands

import rethinkdb
from rethinkdb.errors import ReqlDriverError, ReqlRuntimeError


class Bot(commands.Bot):
    """Bot class of Rotom, pretty self-explainatory"""

    def __init__(self, config_file: str='config.yml', **options):
        # For selfbots
        bot = options.get('bot', True)

        # Setting up language packs
        self._lang = self.load_lang('lang')
        self.t = self._lang.get

        # Setting up logging
        file_hdlr = logging.FileHandler(
            filename='LOG', encoding='utf-8', mode='a')
        stream_hdlr = logging.StreamHandler()

        formatter = logging.Formatter(
            fmt='[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='GMT%z %Y-%m-%d %I:%M:%S%p')
        file_hdlr.setFormatter(formatter)
        stream_hdlr.setFormatter(formatter)

        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        self.log.addHandler(file_hdlr)
        self.log.addHandler(stream_hdlr)

        self.log.info(self.t('logging.success'))

        # Loading config file. if the bot can't search for config file
        # with the passed filename, find template config file and rename it
        # to the provided filename if the token isn't empty.
        try:
            self.log.info(self.t('config.loading').format(config_file))

            with open(config_file, 'r') as c_yaml:
                self.config = yaml.load(c_yaml)
                self.log.info(self.t('config.success'))

            if self.config['token'] is None:
                self.log.error(self.t('config.no_token_error').format(config_file))

        except FileNotFoundError:
            self.log.error(self.t('config.file_not_found').format(config_file))

            try:
                self.log.info(self.t('config.loading').format('config_template.yml'))

                with open('config_template.yml', 'r') as c_yaml:
                    self.config = yaml.load(c_yaml)
                    self.log.info(self.t('config.success'))
                    self.log.info(self.t('config.check_token'))

                    if self.config['token'] is not None:
                        self.log.info(self.t('config.token_found'))
                        self.log.info(self.t('config.rename').format('config_template.yml', config_file))
                        os.rename('config_template.yaml', config_file)
                    else:
                        self.log.error(self.t('config.no_token_error').format('config.template.yml'))
                        sys.exit()

            except FileNotFoundError:
                self.log.error(self.t('config.file_not_found').format('config_template.yml'))
                self.log.error(self.t())
                sys.exit()

        # Initializing commands.Bot
        super().__init__(
            command_prefix=commands.when_mentioned_or(), **options)
        self.log.info(self.t('bot.initialized'))

        # Initialize database
        try:
            self.log.info(self.t('db.connecting').format(
                self.config['db']['host'],
                self.config['db']['port']))
            # Check if passwd is empty first before checking user
            # Since RethinkDB can work with just username only
            if self.config['db']['passwd'] is None:
                if self.config['db']['user'] is None:
                    self.config['db']['user'] = 'admin'
                self._db_conn = rethinkdb.connect(
                    self.config['db']['host'],
                    self.config['db']['port']
                    self.config['db']['user'])
            else:
                self._db_conn = rethinkdb.connect(
                    self.config['db']['host'],
                    self.config['db']['port']),
                    user=self.config['db']['user'],
                    password=self.config['db']['passwd'])
            self.log.info(self.t('db.connect_success'))
        except ReqlDriverError:
            self.log.error(self.t('db.connect_fail'))
            sys.exit()

        try:
            self.db = self._db_conn.db_create(self.config['db']['name'])
            self.log.info(self.t('db.created_db').format(self.config['db']['name']))
        except ReqlRuntimeError:
            self.db = self._db_conn.db(self.config['db']['name'])
            self.log.info(self.t('db.db_exist').format(self.config['db']['name']))
        
    # Some discord.Embed objects with custom colors here

    def load_lang(self, path: str):
        """Loads all available language packs."""
        for a in os.scandir('lang'):
            if a.is_dir():
                self._lang.update(
                    { a.name: Language(a) }
                )

    def get_lang(self, filename: str):
        """Returns the strings of matching filename in dictionary."""
        return Coglang(self._lang, filename)
                        
    def when_mentioned_or(self, *prefixes):
        """Basically the same as `discord.ext.commands.when_mentioned_or` except it also checks for custom per-server prefixes."""
        def inner(bot, msg):
            r = list(prefixes)
            r.append(commands.when_mentioned(bot, msg))
            # If custom prefix is not None:
            # r.append(list(custom_prefix_list))
            return r
        return inner


class Language:
    """Class for language pack"""

    def __init__(self, path):
        self.path = path
        info = None

        # Loads __info__
        for a in os.scandir(self.path):
            if a.is_file() and "__info__" in a.name:
                with open(a.path, 'r') as y:
                    info = yaml.load(y)
        
        # Just in case __info__ isn't available'
        if info is None:
            info = {"name": self.path.name, "author": [None]}
        
        # Turn __info__ attrubutes into Language class''
        self.name = info['name']
        self.author = tuple(info['author'])


class Coglang:
    """Class for cogs language system"""
    def __init__(self, langs: dict, filename: str):
        self._strings = {}

        # Search for file with matching filename in each language pack
        for lang in langs.values():
            for a in os.scandir(lang.path):
                if a.is_file() and filename in a.name:
                    with open(a.path, 'r') as y:
                        self._strings.update(
                            { lang.path.name: yaml.load(y) }
                        )
                # else if there's no filename in the path, ignore it and 
                # check it using try-except + KeyError in get()

    def get(self, key: str, separator: str='.', no_prefix=False):
        """Search for matching key via query and returns it.

        Parameters:
        `key`: `str` - Query that will be used to search for matching key.
        `separator`: `str` - `.` by default, the character that will be used to split the `key` param.
        `no_prefix`: `bool` - `False` by default, check whenether if you want to use the `_prefix` key if it's in the parent key of the requested key.
                              If no prefix was found in the top level object, no prefix will be used."""
        temp = key.split(separator)
        counter = 0

        # Trying to search for prefix in the top level dict
        try:
            if no_prefix:
                prefix = None
            else:
                prefix = self._strings[temp[0]]['_prefix']
        except KeyError:
            prefix = None

        try:
            for k in temp:
                if temp[counter] is k and counter is 0:
                    temp = self._strings[k]
                else:
                    temp = temp[k]
                counter += 1

            if prefix is None:
                return temp
            else:
                return prefix + ' ' + temp
        except KeyError:
            return None

# Builtin commands
class Builtin:
    pass

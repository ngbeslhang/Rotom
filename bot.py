"""Rotom's core"""
import os
import logging
import yaml

import discord
from discord.ext import commands

import rethinkdb
from rethinkdb.errors import ReqlDriverError, ReqlRuntimeError

class Bot(commands.Bot):
    """Bot class of Rotom derived from discord.ext.commands.Bot"""

    def __init__(self, config: str='config.yml', **options):
        """Initialize Rotom.
        
        config : str  - Config file name.
        bot    : bool - Check if the account is a bot, default to `True`."""
        self.bot = options.get('bot', True)

class Language:
    """Class for coglang"""

    def __init__(self, )
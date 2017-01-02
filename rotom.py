"""Rotom's core"""
import os
import argparse
import logging
import yaml

import discord
from discord.ext import commands

import rethinkdb
from rethinkdb.errors import ReqlDriverError, ReqlRuntimeError

class Bot(commands.Bot):
    """Bot class of Rotom derived from discord.ext.commands.Bot"""

    def __init__(self, config: str='config.yml'):
        """Initialize Rotom.
        
        config : str  - Config file name."""
        pass

class Language:
    """Class for coglang"""

    def __init__(self):
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs Rotom.')
    
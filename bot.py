"""Rotom's bot core"""
import asyncio
import logging
import discord
import yaml

from discord.ext import commands

class Bot(commands.Bot):
    """Bot class of Rotom, pretty self-explainatory"""
    def __init__(self, config_file: str='config.yaml', **options):
        # Fetching info from config file, 

        # Initializing commands.Bot
        super().__init__(
            command_prefix=commands.when_mentioned_or(),
            **options
        )

        # Setting up logging
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
    
        self.log.addHandler(logging.StreamHandler())
        self.log.addHandler(logging.FileHandler(filename='LOG'))

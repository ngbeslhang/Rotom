"""Rotom's bot core"""
import os
import sys
#import asyncio
import logging
import yaml
#import discord
from discord.ext import commands


class Bot(commands.Bot):
    """Bot class of Rotom, pretty self-explainatory"""

    def __init__(self, config_file: str='config.yaml', **options):
        # For selfbots
        bot = options.get('bot', True)

        # Setting up language packs

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

        # del formatter, file_hdlr, stream_hdlr # Might have it's use

        self.log.info("[LOGGING] Successfully set up logging system!")

        # Loading config file. if the bot can't search for config file
        # with the passed filename, find template config file and rename it
        # to the provided filename if the token isn't empty.
        try:
            self.log.info("[CONFIG] Attempting to load {}".format(config_file))
            with open(config_file, 'r') as c_yaml:
                self.config = yaml.load(c_yaml)
                self.load.info("[CONFIG] Success!")
        except FileNotFoundError:
            self.log.error("[CONFIG] Unable to find {}!".format(config_file))
            try:
                self.log.info(
                    "[CONFIG] Attempting to load the template config file...")
                with open('config_template.yaml', 'r') as c_yaml:
                    self.config = yaml.load(c_yaml)
                    self.log.info("[CONFIG] Success!")
                    self.log.info("[CONFIG] Checking if token isn't empty...")

                    if self.config['token'] is not None:
                        self.log.info(
                            "[CONFIG] Token isn't empty, the template config file "
                            "will be renamed to the filename you have passed.")
                        os.rename('config_template.yaml', config_file)
                    else:
                        self.log.error(
                            "[CONFIG] Please provide a token in the config file."
                        )
                        sys.exit()
            except FileNotFoundError:
                self.log.error("[CONFIG] Unable to find template config file! "
                               "Please make sure that either config.yaml or "
                               "config_template.yaml exist. You can check the "
                               "GitHub repo for the config template.")
                sys.exit()

        # Initializing commands.Bot
        super().__init__(
            command_prefix=commands.when_mentioned_or(), **options)
        self.log.info("Self-initialized!")

        # Initialize database

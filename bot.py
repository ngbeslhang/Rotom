"""Rotom's core"""
import asyncio
import discord

class Bot(discord.ext.commands.AutoShardedBot):
    def __init__(self, conf, debug):
        # Initializations
        self.boot_time = __import__('time').time()

    # TODO: Modify the extension import/export functions
    # TODO: Write a custom command class?

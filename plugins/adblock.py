from discord.ext import commands

class MsgBlock:
    def __init__(self):
        self.dependancy = ['local_config']
        # multidir plugins are supported
        # to import only a specific part of plugin just type them as if you are importing them in Python e.g. plugin.sub
        # if only the parent module is imported, setup() must be in __init__.py
        # If there's none bot will return an error implying that the plugin doesn't support import-all
        # if there's no self.dependancy the plugin will be imported w/o dep checks
        # Otherwise the bot will attempt to import all deps until it suceed or fail
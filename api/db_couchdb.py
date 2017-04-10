"""Couchbase database cog for Rotom"""
import aiohttp
import json

class DB:
    """Database module for Rotom."""

    def __init__(self, bot):
        self.bot = bot
        self.bot.db = self
        self.bot.loop.run_until_complete(self.init_db())
            
    async def init_db(self):
        self._session = aiohttp.ClientSession(loop=self.bot.loop)
        self._url = "http://{0[host]}:{0[port]}/{0[db]}".format(self.bot.get_api_conf())

        async with self._session.get(self._url) as r:
            if r.status != 200:
                self.bot.log.error("[DB] Unable to connect to the database! Are you sure it's launched?")
                self.bot.db = None
            else:
                content = json.loads(r.content)

                try:
                    if content['ok'] is True:
                        self.bot.log.info("[DB] Successfully connected to database!")
                except KeyError:
                    if content['error'] == "not_found":
                        self.bot.log.warning("[DB] Database not found! A new one will be created instead.")

                        async with self._session.put(self._url) as c:
                            if r.status != 200:
                                self.bot.log.error("[DB] Unable to connect to the database!")
                                self.bot.db = None
                            else:
                                d = json.loads(c.content)
                                try:
                                    if content['ok'] is True:
                                        self.bot.log.info("[DB] Database successfully created!")
                                except KeyError:
                                    self.bot.log.error("[DB] Unable to create database!")
                                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(d))
                                    self.bot.db = None
                    else:
                        self.bot.log.error("[DB] Error!")
                        self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(content))
                        self.bot.db = None
    
    async def insert(self, id, key, value):
        pass

    async def edit(self, id, key, value):
        """Edits the key with a new value.
        
        `id` - The object ID.
        `key` - The key name.
        `value` - The new value which will be assigned to the key.
        **NOTE**: If the ID/key doesn't exist it will be created instead."""
        pass


    async def get(self, table, key):
        pass

    async def delete(self, table, key):
        pass


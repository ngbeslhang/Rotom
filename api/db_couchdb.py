"""Couchbase database cog for Rotom"""
import aiohttp
import json
from discord import Server, Channel, PrivateChannel, Member, User, ChannelType

class DB:
    """Database module for Rotom."""

    def __init__(self, bot):
        self.bot = bot
        self.bot.db = self
        self.bot.loop.run_until_complete(self.init_db())
            
    async def init_db(self):
        self._session = aiohttp.ClientSession(loop=self.bot.loop)
        self._url = "http://{0[host]}:{0[port]}/{0[db]}".format(self.bot.get_api_conf())

        try:
            async with self._session.get(self._url) as r:
                if r.status == 200:
                     self.bot.log.info("[DB] Successfully connected to database!")
                elif r.status == 404:
                    self.bot.log.warning("[DB] Database not found! A new one will be created instead.")

                    async with self._session.put(self._url) as r:
                        if r.status == 201:
                            self.bot.log.info("[DB] Database successfully created!")
                        else:
                            self.bot.log.error("[DB] Unable to create database!")
                            async for line in r.content:
                                temp = json.loads(line)
                            self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
                            self.bot.db = None
                else:
                    self.bot.log.error("[DB] Unknown error!")
                    async for line in r.content:
                        temp = json.loads(line)
                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
                    self.bot.db = None
        except Exception as e:
            self.bot.log.error("[DB] Unable to connect to the database! Are you sure it's launched?")
            self.bot.db = None
            self.bot.log.error("[DB] Unknown error while trying to connect to server!")
            self.bot.log.error("Error: {}, Reason: {}".format(type(e).__name__, str(e)))

    
    async def create(self, obj, data: dict={}):
        """Creates a new database object.

        `obj` - The object, either `discord.Server`, `discord.Channel/Channel` or `discord.User/Member`.
        `data`: dict - The data to initialize the object with.
        **NOTE**: `data` will be updated with `obj`'s attributes."""

        data.update({
            "id": obj.id,
        })

        # Server/User obj wouldn't need additional data update here
        if type(obj) in (Channel, PrivateChannel):
            if obj.type in (ChannelType.text, ChannelType.voice):
                data.update({
                    "server": obj.server.id,
                    "type": str(obj.type)
                })
            elif obj.type in (ChannelType.private, ChannelType.group):
                data.update({
                    "type": str(obj.type)
                })
        elif type(obj) is Member:
            data.update({
                "servers": {
                    str(obj.server.id): {}
                }
            })
        else:
            raise ValueError("The object must be either discord.Server, discord.Channel or discord.User.")
            return

        try:
            async with self._session.put(self._url+"/{}".format(obj.id), data=data) as r:
                if r.status == 201:
                    self.bot.log.info("[DB] Object successfully created")
                else:
                    self.bot.log.error("[DB] Unable to create object!")
                    async for line in r.content:
                        temp = json.loads(line)
                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
                    self.bot.db = None
        except Exception as e:
            self.bot.log.error("[DB] Unknown error while trying to create object!")
            self.bot.db = None
            self.bot.log.error("Error: {}, Reason: {}".format(type(e).__name__, str(e)))

    async def update(self, obj, data: dict):
        """Updates the object with provided dictionary.

        `id` - The object or its ID (either int or str), usually discord.py objects'.
        `obj`: dict - The dictionary to update the object with."""

        if type(obj) in (Server, Channel, PrivateChannel, Member, User):
            obj = obj.id
        elif type(obj) in (str, int):
            pass
        else:
            raise ValueError("The object must be either discord.Server/Channel/User, int or str.")
            return

        try:
            async with self._session.get(self._url+"/{}".format(obj.id)) as r:
                async for line in r.content:
                    temp = json.loads(line)

                if r.status == 200:
                    data.update({
                        "_rev": temp['_rev']
                    })
                else:
                    self.bot.log.error("[DB] Unable to update object!")
                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
                    self.bot.db = None
            
            async with self._session.put(self._url+"/{}".format(obj.id), data=data) as r:
                if r.status == 201:
                    self.bot.log.info("[DB] Object successfully updated")
                else:
                    self.bot.log.error("[DB] Unable to update object!")
                    async for line in r.content:
                        temp = json.loads(line)
                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
                    self.bot.db = None
        except Exception as e:
            self.bot.log.error("[DB] Unknown error while trying to update object!")
            self.bot.db = None
            self.bot.log.error("Error: {}, Reason: {}".format(type(e).__name__, str(e)))


    async def get(self, id, key):
         """Updates the object with provided dictionary.

        `id` - The object or its ID (either int or str), usually discord.py objects'.
        `obj`: dict - The dictionary to update the object with."""

        if type(obj) in (Server, Channel, PrivateChannel, Member, User):
            obj = obj.id
        elif type(obj) in (str, int):
            pass
        else:
            raise ValueError("The object must be either discord.Server/Channel/User, int or str.")
            return

        try:
            async with self._session.get(self._url+"/{}".format(obj.id)) as r:
                async for line in r.content:
                    temp = json.loads(line)

                if r.status == 200:
                    self.bot.log.info("[DB] Object successfully fetched")
                    return temp
                else:
                    self.bot.log.error("[DB] Unable to get object!")
                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
        except Exception as e:
            self.bot.log.error("[DB] Unknown error while trying to get object!")
            self.bot.db = None
            self.bot.log.error("Error: {}, Reason: {}".format(type(e).__name__, str(e)))

    async def delete(self, id, key):
        pass


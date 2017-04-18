"""Couchbase database cog for Rotom"""
import aiohttp
import json
from discord import Server, Channel, PrivateChannel, Member, User, ChannelType


class DB:
    """Database module for Rotom."""

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.run_until_complete(self.init_db())

    async def init_db(self):
        self._session = aiohttp.ClientSession(loop=self.bot.loop)
        self._url = "http://{0[host]}:{0[port]}/{0[db]}".format(self.bot.get_api_conf())

        try:
            async with self._session.get(self._url) as r:
                if r.status == 200:
                    self.bot.log.info("[DB] Successfully connected to database!")
                    self.bot.db = self
                elif r.status == 404:
                    self.bot.log.warning(
                        "[DB] Database not found! A new one will be created instead.")

                    async with self._session.put(self._url) as r:
                        if r.status == 201:
                            self.bot.log.info("[DB] Database successfully created!")
                            self.bot.db = self
                        else:
                            self.bot.log.error("[DB] Unable to create database!")
                            temp = None
                            async for line in r.content:
                                temp = json.loads(line)
                            self.bot.log.error(
                                "[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
                else:
                    self.bot.log.error("[DB] Unknown error!")
                    temp = None
                    async for line in r.content:
                        temp = json.loads(line)
                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
        except Exception as e:
            self.bot.log.error(
                "[DB] Unable to connect to the database! Are you sure it's launched?")
            self.bot.log.error("[DB] Unknown error while trying to connect to server!")
            self.bot.log.error("Error: {}, Reason: {}".format(type(e).__name__, str(e)))

    async def create(self, obj, data: dict={}):
        """Creates a new database object.

        `obj` - The object or its ID (either int or str), usually discord.py objects'.
        `data`: dict - The data to initialize the object with.
        **NOTE**: `data` will be updated with `obj`'s attributes."""

        if type(obj) not in (str, int):
            data.update({"id": obj.id, })

        # Server/User obj wouldn't need additional data update here
        if type(obj) in (Channel, PrivateChannel):
            if obj.type in (ChannelType.text, ChannelType.voice):
                data.update({"server": obj.server.id, "type": str(obj.type)})
            elif obj.type in (ChannelType.private, ChannelType.group):
                data.update({"type": str(obj.type)})
        elif type(obj) is Member:
            data.update({"servers": {str(obj.server.id): {}}})
        elif type(obj) in (str, int):
            pass
        else:
            raise ValueError(
                "The object must be either discord.Server, discord.Channel or discord.User.")
            return

        try:
            async with self._session.put(self._url + "/{}".format(obj.id), data=data) as r:
                if r.status in (201, 202):
                    self.bot.log.info("[DB] Object successfully created")
                    return True
                elif r.status == 409:
                    self.bot.log.info("[DB] Object conflict!")
                    return False
                else:
                    self.bot.log.error("[DB] Unable to create object!")
                    temp = None
                    async for line in r.content:
                        temp = json.loads(line)
                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
                    return False
        except Exception as e:
            self.bot.log.error("[DB] Unknown error while trying to create object!")
            self.bot.log.error("Error: {}, Reason: {}".format(type(e).__name__, str(e)))
            return False

    async def update(self, obj, data: dict):
        """Updates the object with provided dictionary.

        `obj` - The object or its ID (either int or str), usually discord.py objects'.
        `data`: dict - The dictionary to update the object with."""

        if type(obj) in (Server, Channel, PrivateChannel, Member, User):
            obj = obj.id
        elif type(obj) in (str, int):
            pass
        else:
            raise ValueError("The object must be either discord.Server/Channel/User, int or str.")
            return False

        try:
            async with self._session.get(self._url + "/{}".format(obj.id)) as r:
                temp = None
                async for line in r.content:
                    temp = json.loads(line)

                if r.status == 200:
                    data.update({"_rev": temp['_rev']})
                elif r.status == 404:
                    return False
                else:
                    self.bot.log.error("[DB] Unable to update object!")
                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
                    return False

            async with self._session.put(self._url + "/{}".format(obj.id), data=data) as r:
                if r.status in (201, 202):
                    self.bot.log.info("[DB] Object successfully updated")
                    return True
                elif r.status == 409:
                    self.bot.log.info("[DB] Object conflict!")
                    return False
                else:
                    self.bot.log.error("[DB] Unable to update object!")
                    temp = None
                    async for line in r.content:
                        temp = json.loads(line)
                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
                    return False
        except Exception as e:
            self.bot.log.error("[DB] Unknown error while trying to update object!")
            self.bot.log.error("Error: {}, Reason: {}".format(type(e).__name__, str(e)))
            raise e
            return False

    async def get(self, obj, key=""):
        """Get object in dictionary form.

        `obj`: dict - The dictionary to update the object with."""
        if type(obj) in (Server, Channel, PrivateChannel, Member, User):
            obj = obj.id
        elif type(obj) in (str, int):
            pass
        else:
            raise ValueError("The object must be either discord.Server/Channel/User, int or str.")

        try:
            async with self._session.get(self._url + "/{}".format(obj.id)) as r:
                temp = None
                async for line in r.content:
                    temp = json.loads(line)

                if r.status == 200:
                    self.bot.log.info("[DB] Object successfully fetched")
                    return temp
                else:
                    self.bot.log.error("[DB] Unable to get object!")
                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
                    return None
        except Exception as e:
            self.bot.log.error("[DB] Unknown error while trying to get object!")
            self.bot.log.error("Error: {}, Reason: {}".format(type(e).__name__, str(e)))
            return None

    async def delete(self, obj):
        """Delete the object from database.

        `obj` - The object or its ID (either int or str), usually discord.py objects'."""

        if type(obj) in (Server, Channel, PrivateChannel, Member, User):
            obj = obj.id
        elif type(obj) in (str, int):
            pass
        else:
            raise ValueError("The object must be either discord.Server/Channel/User, int or str.")
        
        rev = None

        try:
            async with self._session.get(self._url + "/{}".format(obj.id)) as r:
                temp = None
                async for line in r.content:
                    temp = json.loads(line)

                if r.status == 200:
                    rev = temp['_rev']
                else:
                    self.bot.log.error("[DB] Unable to update object!")
                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
                    return False

            async with self._session.put(self._url + "/{}?rev={}".format(obj.id, rev)) as r:
                if r.status == 200:
                    self.bot.log.info("[DB] Object successfully updated")
                    return True
                else:
                    self.bot.log.error("[DB] Unable to update object!")
                    temp = None
                    async for line in r.content:
                        temp = json.loads(line)
                    self.bot.log.error("[DB] Error: {0[error]} | Reason: {0[reason]}".format(temp))
                    return False
        except Exception as e:
            self.bot.log.error("[DB] Unknown error while trying to update object!")
            self.bot.log.error("Error: {}, Reason: {}".format(type(e).__name__, str(e)))
            raise e
            return False

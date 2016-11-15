"""db_couchdb.py - CouchDB wrapper for Rotom"""
import discord
import couchdb

required = ["couchdb"]


class DB:
    """Database class."""

    def __init__(self, name, host, port, user, passwd):
        """Connects to the server and create a database for the bot."""
        if user and passwd != None:
            url = "https://{}:{}@{}:{}".format(user, passwd, host, port)
        elif user != None:
            url = "https://{}@{}:{}".format(user, host, port)
        else:
            url = "https://{}:{}".format(host, port)

        self._server = couchdb.Server(url)
        del url

        try:
            self._db = self._server.create(name)
        except couchdb.PreconditionFailed:
            self._db = self._server[name]

    def insert(self, d: dict, obj):
        if isinstance(obj, discord.Server):
            name = 'server'
        elif isinstance(obj, discord.Channel):
            name = 'channel'
        elif isinstance(obj, discord.Member) or isinstance(obj, discord.PrivateChannel):
            name = 'user'
        else:
            # raise Exception
            return

        upload = { "_id": name + "." + obj.id }
        upload.update(d)
        self._db.save(upload)

    def find(self, d, object):
        if isinstance(d, list):
            result = {}

        if result != []:
            if d in self._db:
                return self._db[d]
            else:
                for k in self._db:
                    if d in k:
                        return self._db[k]
        else:
            for k in d:
                if k in self._db:
                    result.update({k: self._db[k]})
                else:
                    for s in self._db:
                        if k in s:
                            result.update({s: self._db[s]})
        return result
        
"""db_couchdb.py - CouchDB wrapper for Rotom"""
import couchdb

required = ["couchdb"]

class DB:
    def __init__(self, name, host, port, user, passwd):
        """
        Connects to the server and create a database for the bot.
        """
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
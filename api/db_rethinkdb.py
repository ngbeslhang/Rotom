"""RethinkDB database cog for Rotom"""
import rethinkdb
from rethinkdb.errors import ReqlDriverError, ReqlRuntimeError

# Using async for RethinkDB
rethinkdb.set_loop_type("asyncio")


class DB:
    """RethinkDB module for Rotom."""

    def __init__(self, bot):
        self.bot = bot
        self.conn = rethinkdb.connect()
        self.bot.db


#name   : rotom
#host   : localhost
#port   : 28015
#user   : ~
#passwd : ~
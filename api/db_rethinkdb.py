"""RethinkDB database cog for Rotom"""
import asyncio
import rethinkdb
from rethinkdb.errors import ReqlDriverError, ReqlRuntimeError

# Using async for RethinkDB
rethinkdb.set_loop_type("asyncio")


class DB:
    """RethinkDB module for Rotom."""

    def __init__(self, bot):
        self.bot = bot
        self.conn = rethinkdb.connect()
        bot.db = self
    
    @asyncio.coroutine
    def create(self, table, key, value):
        """Creates a new key with the value.
        
        `table`
        `key` - The key name.
        `value` - The value which will be assigned to the key.
        **NOTE**:"""
        pass
    
    @asyncio.coroutine
    def edit(self, table, key, value):
        """Edits the key with a new value.
        
        `table` - The table name, usually the server ID.
        `key` - The key name.
        `value` - The new value which will be assigned to the key."""
        pass

    @asyncio.coroutine
    def get(self, table, key):
        pass

    @asyncio.coroutine
    def delete(self, table, key):
        pass

#name   : rotom
#host   : localhost
#port   : 28015
#user   : ~
#passwd : ~
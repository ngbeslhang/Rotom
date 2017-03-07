"""PostgreSQL database cog for Rotom using asyncpg"""
import asyncio
import asyncpg


class DB:
    """RethinkDB module for Rotom."""

    def __init__(self, bot):
        self.bot = bot
        self.connection = await asyncpg.create_pool()
        bot.db = self
    
    async def create(self, table, key, value):
        """Creates a new key with the value.
        
        `table`
        `key` - The key name.
        `value` - The value which will be assigned to the key.
        **NOTE**:"""
        pass
    
    async def edit(self, table, key, value):
        """Edits the key with a new value.
        
        `table` - The table name, usually the server ID.
        `key` - The key name.
        `value` - The new value which will be assigned to the key."""
        pass


    async def get(self, table, key):
        pass

    async def delete(self, table, key):
        pass


"""Couchbase database cog for Rotom"""


class DB:
    """Database module for Rotom."""

    def __init__(self, bot):
        self.bot = bot
        bot.db = self
    
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


"""PostgreSQL database cog for Rotom using asyncpg"""
import asyncpg


class DB:
    """PostgreSQL module for Rotom."""

    def __init__(self, bot):
        self.bot = bot
        bot.db = self
        self.bot.loop.run_until_complete(self._connect())

    async def _connect(self):
        conf = self.bot.get_api_conf()

        # It should work, right? *right?*
        if conf['dsn'] is not None:
            self.conn = await asyncpg.connect(dsn=conf['dsn'])
        else:
            self.conn = await asyncpg.connect(
                host=conf['host'],
                port=conf['port'],
                user=conf['user'],
                password=conf['passwd'],
                database=conf['db'],
            )
    
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


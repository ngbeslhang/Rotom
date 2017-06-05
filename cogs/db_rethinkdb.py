import rethinkdb as r
r.set_loop_type('asyncio')

class DB:
    def __init__(self, bot):
        self.bot = bot
        bot.loop.run_until_complete(self._init())

    async def _init(self):
        self._conf = self.bot.get_conf()
        try:
            conn = await r.connect(host=self._conf['host'], port=self._conf['port'], db=self._conf['name'])
            self.bot.log.info("[RethinkDB] Successfully connected!")
            await conn.close()
            self.bot.db = self
        except r.RqlDriverError:
            try:
                self.bot.log.info("[RethinkDB] Database not created yet, creating...")
                conn = await r.connect(host=self._conf['host'], port=self._conf['port'])
                r.db_create(self._conf['name'])
                self.bot.log.info("[RethinkDB] Successfully connected and created database!")
                await conn.close()
                self.bot.db = self
            except r.RqlDriverError:
                self.bot.log.error("[RethinkDB] Unable to connect to database!")
        except TypeError:
            self.bot.log.error("[RethinkDB] Config does not exist!")

    # Based on https://rethinkdb.com/docs/sql-to-reql/python/
    # The reason why the id param of all db operation funcs here uses int is based on discord.py rewrite's decision
    # of using int for all Discord object IDs. For legacy/async pass int(discord.[Object].id) instead.

    async def select(self, table: str, id: int):
        """Selects document with given ID from given table and returns the data in the form of dict.

        table : str - Table name.
        id    : int - Document ID."""

    async def insert(self, table: str, id: int, data: dict):
        """Insert document into given table with given ID.
        If given table doesn't exists make a new table and insert the document with given ID.

        table : str  - Table name.
        id    : int  - Document ID.
        data  : dict - Document data."""

    async def update(self, table: str, id: int, data: dict):
        """Update document with given ID in given table with new given data.
        
        table : str  - Table name.
        id    : int  - Document ID.
        data  : dict - Document data."""

    async def delete(self, table: str, id: int):
        """Delete document with given ID from the given table.

        table : str - Table name.
        id    : int - Document ID."""

    async def _eval(self, code: str):
        """Evaluate database code with the built-in eval command and returns the result.
        
        code : str - Code to evaluate."""


def setup(bot):
    bot.add_cog(DB(bot))
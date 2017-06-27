import rethinkdb as r
r.set_loop_type('asyncio')

class DB:
    def __init__(self, bot):
        self.bot = bot
        self._conf = self.bot.get_conf()
        bot.loop.run_until_complete(self._init())

    async def _init(self):
        try:
            conn = await self._connect()
            self.bot.log.info("[RethinkDB] Successfully connected!")
            await conn.close()
            self.bot.db = self
        except r.RqlDriverError:
            self.bot.log.error("[RethinkDB] Unable to connect to database!")
        except TypeError:
            self.bot.log.error("[RethinkDB] Config does not exist!")

    async def _connect(self):
        temp = self._conf
        name = temp['name']
        del temp['name']
        conn = await r.connect(**temp)

        try:
            await conn.use(name)
        except r.RqlDriverError:
            self.bot.log.warning("[RethinkDB] Creating database.")
            await r.db_create(name).run(conn)
            await conn.use(name)

        return conn

    # Based on https://rethinkdb.com/docs/sql-to-reql/python/
    # The reason why the id param of all db operation funcs here uses int is based on discord.py rewrite's decision
    # of using int for all Discord object IDs. For legacy/async pass int(discord.[Object].id) instead.

    async def select(self, tbl: str, name):
        """Selects document with given ID from given table and returns the data in the form of dict.

        tbl : str - Table name.
        name      - Document ID. If int is passed, it will be converted to str.
        
        Exceptions:
        **NOTE**: Only built-in exceptions will be used for maximum modularity.
        `NameError` - Given table does not exist.
        `KeyError` - Given key does not exist."""
        conn = await self._connect()
        t = await r.table(tbl)

        try:
            await t.run(conn)
        except r.errors.ReqlOpFailedError:
            raise NameError("Table {} does not exist.".format(tbl))
        
        if type(name) is int:
            name = str(name)

        result = await t.get(name).run(conn)

        if result is not None:
            return result
        else:
            raise KeyError("Key {} does not exist inside table {}.".format(name, tbl))

    async def write(self, tbl: str, name, data: dict, conflict="update"):
        """Insert document into given table with given ID.
        If given table doesn't exists a new table with the given name will be made and the document with given ID will be inserted.
        If a document with the given name inside the table already exists it will be updated instead by default.

        tbl : str    - Table name.
        name         - Document ID. If int is passed, it will be converted to str.
        data  : dict - Document data.
        conflict     - Ctrl+F `conflict` at https://www.rethinkdb.com/api/python/insert/"""

    async def delete(self, tbl: str, name):
        """Delete document with given ID from the given table.

        tbl : str - Table name.
        name      - Document ID. If int is passed, it will be converted to str."""

    async def _eval(self, code: str):
        """Evaluate database code with the built-in eval command and returns the result.
        
        code : str - Code to evaluate."""


def setup(bot):
    bot.add_cog(DB(bot))
import rethinkdb as r
r.set_loop_type('asyncio')


# Might consider doing https://github.com/dsc/bunch
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
            setattr(self.bot, "db", self)
        except r.RqlDriverError:
            self.bot.log.error("[RethinkDB] Unable to connect to database!")
        except TypeError:
            self.bot.log.error("[RethinkDB] Config does not exist!")

    async def _connect(self):
        """Connect to database"""
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

    def _raise_conn_error(self):
        """Raise ConnectionError if the connection to server fails"""
        self.bot.log.error("[RethinkDB] Unable to connect to database!")
        raise ConnectionError

    # Based on https://rethinkdb.com/docs/sql-to-reql/python/
    # The reason why the id param of all db operation funcs here uses int is based on discord.py rewrite's decision
    # of using int for all Discord object IDs. For legacy/async pass int(discord.[Object].id) instead.

    async def select(self, tbl: str, name):
        """Selects document with given ID from given table and returns the data in the form of dict.

        tbl : str - Table name.
        name      - Document ID. Only str and int are supported.

        Exceptions:
        **NOTE**: Only built-in exceptions will be used for maximum modularity.
        `NameError`       - Given table does not exist.
        `KeyError`        - Given key does not exist.
        `TypeError`       - Passed document ID is not in either str or int type.
        `ConnectionError` - Failed to connect to the database."""
        try:
            conn = await self._connect()
        except r.RqlDriverError:
            self._raise_conn_error()

        try:
            t = await r.table(tbl)

            try:
                await t.run(conn)
            except r.errors.ReqlOpFailedError:
                raise NameError("Table {} does not exist.".format(tbl))

            if type(name) not in (str, int):
                raise TypeError("Document ID must be either str or int.")

            result = await t.get(name).run(conn)

            if result is not None:
                return result
            else:
                raise KeyError("Key {} does not exist inside table {}.".format(name, tbl))
        finally:
            if conn:
                await conn.close()

    async def write(self, tbl: str, data: dict, conflict="update"):
        """Insert document into given table with given ID.
        If given table doesn't exists a new table with the given name will be made and the document with given ID will be inserted.
        If a document with the given name inside the table already exists it will be updated instead by default.

        tbl   : str  - Table name.
        data  : dict - Document data.
        conflict     - Ctrl+F `conflict` at https://www.rethinkdb.com/api/python/insert/

        Exceptions:
        **NOTE**: Only built-in exceptions will be used for maximum modularity.
        `TypeError`       - Passed document ID is not in either str or int type.
        `ConnectionError` - Failed to connect to the database.
        `RuntimeError`    - Failed to insert data, reason included. (Use this if you set `conflict` to `error`)

        **NOTE**: In order to include document ID, please insert `"id": "name"` into `data`.
        The `id` value will be type-checked with only str and int supported.
        If it's not included, RethinkDB will assign a random ID instead.

        **NOTE**: **kwargs support is planned."""
        try:
            conn = await self._connect()
        except r.RqlDriverError:
            self._raise_conn_error()

        try:
            t = await r.table(tbl)

            try:
                await t.run(conn)
            except r.errors.ReqlOpFailedError:
                self.bot.log.info(
                    "[RethinkDB] Table {} does not exist yet, creating...".format(tbl))
                await r.table_create(tbl).run(conn)
                self.bot.log.info("[RethinkDB] Table {} successfully created!".format(tbl))

            try:
                name = data['id']
                if type(name) not in (str, int):
                    raise TypeError("Document ID must be either str or int.")
            except KeyError:
                pass # Since it doesn't quite matter for us to default to randomly assign ID

            try:
                await t.insert(data, conflict=conflict).run(conn)
            except r.errors.ReqlOpFailedError as e:
                raise RuntimeError("Unable to insert value, reason: {}".format(e))
        finally:
            if conn:
                await conn.close()

    async def delete(self, tbl: str, name):
        """Delete document with given ID from the given table.

        tbl : str - Table name.
        name      - Document ID. Only str and int are supported.

        Exceptions:
        **NOTE**: Only built-in exceptions will be used for maximum modularity.
        `NameError`       - Given table does not exist.
        `KeyError`        - Given key does not exist.
        `TypeError`       - Passed document ID is not in either str or int type.
        `ConnectionError` - Failed to connect to the database."""
        try:
            conn = await self._connect()
        except r.RqlDriverError:
            self._raise_conn_error()

        try:
            t = await r.table(tbl)

            try:
                await t.run(conn)
            except r.errors.ReqlOpFailedError:
                raise NameError("Table {} does not exist.".format(tbl))

            if type(name) not in (str, int):
                raise TypeError("Document ID must be either str or int.")

            try:
                await t.get(name).delete().run(conn)
            except r.errors.ReqlOpFailedError as e:
                raise KeyError("Unable to delete key {} inside table {}, reason: {}.".format(name, tbl, e))
        finally:
            if conn:
                await conn.close()

    async def _eval(self, code: str):
        """Evaluate database code with the built-in eval command and returns the result.

        code : str - Code to evaluate."""


def setup(bot):
    bot.add_cog(DB(bot))

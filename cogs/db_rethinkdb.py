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
            conn.close()
        except r.RqlDriverError:
            try:
                self.bot.log.info("[RethinkDB] Database not created yet, creating...")
                self._conn = await r.connect(host=self._conf['host'], port=self._conf['port'])
                r.db_create(self._conf['name'])
                self.bot.log.info("[RethinkDB] Successfully connected and created database!")
            except r.RqlDriverError:
                self.bot.log.error("[RethinkDB] Unable to connect to database!")
        except TypeError:
            self.bot.log.error("[RethinkDB] Config does not exist!")

    # Now should I keep consistent connection or only connect to the db each time I need to use it
    # Using latter
    # https://cdn.discordapp.com/attachments/231823127015981056/314408855779934218/DiscordCanary_2017-05-17_22-28-17.png

    # Based on https://rethinkdb.com/docs/sql-to-reql/python/

    async def update(self, query):
        """A combination of INSERT, UPDATE and DELETE"""

    async def select(self, query):
        """SELECT"""

def setup(bot):
    bot.add_cog(DB(bot))
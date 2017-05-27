import rethinkdb as r
r.set_loop_type('asyncio')

class DB:
    def __init__(self, bot):
        self.bot = bot
        bot.loop.run_until_complete(self._init())

    async def _init(self):
        conf = self.bot.get_conf()
        try:
            self._conn = await r.connect(host=conf['host'], port=conf['port'], db=conf['name'])
            self.bot.log.info("[RethinkDB] Successfully connected!")
        except r.RqlDriverError:
            try:
                self.bot.log.info("[RethinkDB] Database not created yet, creating...")
                self._conn = await r.connect(host=conf['host'], port=conf['port'])
                r.db_create(conf['name'])
                self.bot.log.info("[RethinkDB] Successfully connected and created database!")
            except r.RqlDriverError:
                self.bot.log.error("[RethinkDB] Unable to connect to database!")
        except TypeError:
            self.bot.log.error("[RethinkDB] Config does not exist!")

    # Now should I keep consistent connection or only connect to the db each time I need to use it
    # https://cdn.discordapp.com/attachments/231823127015981056/314408855779934218/DiscordCanary_2017-05-17_22-28-17.png

    async def insert(self, query):
        pass

    async def select(self, query):
        pass

def setup(bot):
    bot.add_cog(DB(bot))
import rethinkdb as r
r.set_loop_type('asyncio')

class DB:
    def __init__(self, bot):
        self.bot = bot
        bot.loop.run_until_complete(self._init())

    async def _init(self):
        try:
            self._conn = r.connect()
        except r.ReqlDriverError:
            self.bot.log.error("[RethinkDB] Unable to connect to database!")

def setup(bot):
    bot.add_cog(DB(bot))
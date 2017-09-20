class Relationship_Log:
    """Logs relationship in light of recent friend req massspam"""
    def __init__(self, bot):
        self.bot = bot

    async def on_relationship_add(self, rel):
        self.bot.log.info(
            "[Relationship] User {0} ({0.id}) added you!".format(rel.user))

    async def on_relationship_removed(self, rel):
        self.bot.log.info(
            "[Relationship] User {0} ({0.id}) removed you!".format(rel.user))

def setup(bot):
    bot.add_cog(Relationship_Log(bot))

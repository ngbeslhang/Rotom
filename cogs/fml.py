import discord
import asyncio

class FML:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, msg):
        if msg.content == "I agree to the terms and conditions" and msg.channel.id == 349198111345868801:
            role = [i for i in msg.guild.roles if i.id == 349077573977899011]
            asyncio.sleep(2)
            usr_role = [i for i in msg.author.roles if i.id == 349077573977899011]
            if not usr_role:
                msg.author.edit(
                roles=msg.author.roles+role,
                reason="[VerifyBackup] User agreed to terms but Bronzong have issues granting role.")

def setup(bot):
    bot.add_cog(FML(bot))

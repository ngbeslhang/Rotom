# Ad-block module for Rotom since StahpDozAds is dead and I need it
import discord
from discord.errors import Forbidden, NotFound, InvalidArgument

class NoAd:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, msg):
        roles = ['111505380638519296',
                 '117242433091141636',
                 '126430648951898112',
                 '278331223775117313']

        if msg.server.id == '111504456838819840':
            if "discord.gg/pokemon" not in msg.content:
                if ("discord.gg/" in msg.content and 
                        [r.id for r in msg.author.roles] not in roles or
                        msg.channel.id != '270033143996612608'):
                            await self.bot.delete_message(msg)
                            await self.bot.send_message(msg.channel, 
                                "{0} Your message has been deleted because: Your message contains an invite link.".format(msg.author.mention))

                            try:
                                em = discord.Embed(title="SOMEONE POSTED AN INVITE")
                                em.add_field("Content", msg.content)
                                em.add_field("Message ID", msg.id, inline=True)
                                em.add_field("Posted at", msg.channel.name, inline=True)

                                await self.bot.send_message(
                                    msg.server.get_channel('272438017745223681'),
                                    "{0.name} `{0.id}`".format(msg.author),
                                    embed=em
                                )
                            except (Forbidden, NotFound, InvalidArgument):
                                self.bot.log.warning("[NoAd] Channel not found!")
                                
                            self.bot.log.info("[NoAd] User: {0.name} ({0.id})".format(msg.author))
                            self.bot.log.info("[NoAd] Content: {0.content}".format(msg))
                            self.bot.log.info("[NoAd] At: {0.name} ({0.id})".format(msg.channel))
                                

def setup(bot):
    bot.add_cog(NoAd(bot))
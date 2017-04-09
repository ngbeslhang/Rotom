# Ad-block module for Rotom since StahpDozAds is dead and I need it
import discord
from discord.errors import Forbidden, NotFound, InvalidArgument

class NoAd:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, msg):
        roles = [s.id for s in msg.server.roles if s.name.lower() in ["mods", "reddit mods", "bots", "regoodras"]]

        # 111504456838819840 Pokemon discord
        if msg.server.id == '180250773181956096':
            if "discord.gg/" in msg.content:
                if "discord.gg/pokemon" not in msg.content:
                    # 270033143996612608
                    if msg.channel.id != '180261884979576832':
                        if any(e in [r.id for r in msg.author.roles] for e in roles) is False:
                            self.bot.send_message(msg.channel, "```{}```".format([r.id for r in msg.author.roles]))
                            self.bot.send_message(msg.channel, "```{}```".format(roles))
                            await self.bot.delete_message(msg)
                            await self.bot.send_message(msg.channel, 
                                "{0} Your message has been deleted because: Your message contains an invite link.".format(msg.author.mention))

                            try:
                                em = discord.Embed(title="SOMEONE POSTED AN INVITE")
                                em.add_field(name="Content", value=msg.content, inline=False)
                                em.add_field(name="Message ID", value=msg.id)
                                em.add_field(name="Posted at", value=msg.channel.name)

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
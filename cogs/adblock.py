# Ad-block module for Rotom since StahpDozAds is dead and I need it
import discord
from discord.errors import Forbidden, NotFound, InvalidArgument

class NoAd:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, msg):
        roles = ['111505380638519296', '117242433091141636', '126430648951898112', '278331223775117313']

        if msg.server.id == '111504456838819840':
            if "discord.gg/" in msg.content:
                if "discord.gg/pokemon" not in msg.content:
                    if msg.channel.id != '270033143996612608':
                        if any(e in [r.id for r in msg.author.roles] for e in roles) is False:
                            await self.bot.delete_message(msg)
                            await self.bot.send_message(msg.channel, 
                                "{0} Your message has been deleted because: Your message contains an invite link.".format(msg.author.mention))

                            try:
                                em = discord.Embed(colour=discord.Colour(value=None).orange())

                                if msg.author.avatar_url is not None:
                                    em.set_author(name=str(msg.author), icon_url=msg.author.avatar_url)
                                else:
                                    em.set_author(name=msg.author.name, icon_url=msg.author.default_avatar_url)
                                em.add_field(name="Content", value=msg.content, inline=False)
                                em.add_field(name="User ID", value=msg.author.id)
                                em.add_field(name="Message ID", value=msg.id)
                                em.add_field(name="Posted at", value=msg.channel.name)

                                await self.bot.send_message(
                                    msg.server.get_channel('272438017745223681'),
                                    None, embed=em
                                )
                            except (Forbidden, NotFound, InvalidArgument):
                                self.bot.log.warning("[NoAd] Channel not found!")
                                
                            self.bot.log.info("[NoAd] User: {0.name} ({0.id})".format(msg.author))
                            self.bot.log.info("[NoAd] Content: {0.content}".format(msg))
                            self.bot.log.info("[NoAd] At: {0.name} ({0.id})".format(msg.channel))
                                

def setup(bot):
    bot.add_cog(NoAd(bot))

# Planning to add memedog block feature
"""
╭━━━━╮               This is memedog. Help
╰┃ ┣▇━▇                memedog take over 
 ┃ ┃  ╰━▅╮ Discord by pasting
 ╰┳╯ ╰━━┳╯ him in 10 other
  ╰╮ ┳━━╯     servers or he will
 ▕▔▋ ╰╮╭━╮ never be a memedog
╱▔╲▋╰━┻┻╮╲╱▔▔▔╲
▏  ▔▔▔▔▔▔▔  O O┃ 
╲╱▔╲▂▂▂▂╱▔╲▂▂▂╱
 ▏╳▕▇▇▕ ▏╳▕▇▇▕
 ╲▂╱╲▂╱ ╲▂╱╲▂╱
"""
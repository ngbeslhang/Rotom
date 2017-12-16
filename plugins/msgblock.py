import discord
from discord.ext import commands
from ruamel import yaml
import re

class MsgBlock:
    def __init__(self, bot):
        self.bot = bot
        self.info = {
            
        }
        self.discord_re = re.compile(
            r"(discord\.gg\/|discordapp\.com/invite/|discord\.com/invite/)(\S+)",
            re.IGNORECASE)
        self.roles = [111505380638519296,
                      117242433091141636,
                      126430648951898112,
                      278331223775117313]
        self.bypass_server = [175094349116342274,
                              146626123990564864,
                              111504456838819840]

    async def on_message(self, msg):
        if msg.guild is None:
            return
        
        if msg.guild.id == 111504456838819840 and msg.channel.id != 270033143996612608:
            if not any(e in [r.id for r in msg.author.roles] for e in self.roles):
                # Invte detection
                inv = self.discord_re.findall(self._embed_extractor(msg))
                c = self.bot.get_channel(328507346655641601)
                if inv:
                    for l, i in inv:
                        try:
                            a = await self.bot.get_invite(i)
                            if a.guild.id not in self.bypass_server:
                                em = discord.Embed(colour=discord.Colour.orange())

                                if msg.author.avatar_url is not None:
                                    em.set_author(name=str(msg.author), icon_url=msg.author.avatar_url)
                                else:
                                    em.set_author(name=str(msg.author), icon_url=msg.author.default_avatar_url)
                                
                                await msg.delete()
                                # Yes I know
                                await msg.channel.send(
                                    "{}'s message has been deleted due to: contains an unauthorized invite link.".format(
                                    msg.author.mention))
                                em.title = "Message deleted for unauthorized invite link"

                                em.add_field(name="Content", value=msg.content, inline=False)
                                em.add_field(name="User ID", value=msg.author.id)
                                em.add_field(name="Message ID", value=msg.id)
                                em.add_field(name="Posted at", value=msg.channel.name)

                                await c.send(embed=em)
                        except (discord.NotFound, discord.HTTPException):
                            pass # We don't really need it

                # Mention spamming detection
                if msg.mentions and len(msg.mentions) >= 5:
                    em = discord.Embed(colour=discord.Colour.red())

                    if len(msg.mentions) >= 8 or len(msg.raw_role_mentions) >= 3:
                        await msg.author.ban(
                            reason="[ROTOM] Mass pings detected, see #d-rotom_logs for details.",
                            delete_message_days=0)
                        await msg.channel.send(
                            "{} has been banned due to: mass pings.".format(
                            msg.author.mention))
                        em.title = "Banned for mass ping spam"
                    else:
                        await msg.author.send("You have been kicked for excessive mentions.")
                        await msg.author.kick(
                            reason="[ROTOM] Excessive pings detected, see #d-rotom_logs for details.")
                        await msg.channel.send(
                            "{} has been kicked due to: excessive pings.".format(
                                msg.author.mention))
                        em.title = "Kicked for excessive spam"

                    if msg.author.avatar_url is not None:
                        em.set_author(name=str(msg.author), icon_url=msg.author.avatar_url)
                    else:
                        em.set_author(name=str(msg.author), icon_url=msg.author.default_avatar_url)
                    em.add_field(name="Content", value=msg.content, inline=False)
                    em.add_field(name="User ID", value=msg.author.id)
                    em.add_field(name="Message ID", value=msg.id)
                    em.add_field(name="Posted at", value=msg.channel.name)

                    await c.send(embed=em)


    def _embed_extractor(self, msg):
        """Extracts all content inside an embed if there's any.

        Returns
        -------
        content
            The message content and (if any) all embed contents."""
        if not msg.embeds:
            return msg.content

        content = msg.content + '\n'
        for em in msg.embeds:
            e = em.to_dict()
            for k, v in e.items():
                if k in ['title', 'description', 'url']:
                    content += v + '\n'
                elif k is 'footer':
                    content += v['text'] + '\n'
                elif k is 'author':
                    content += v['name'] + ' | ' + v['url'] + '\n'
                elif k is 'fields' and v != []:
                    for f in e['fields']:
                        for key, val in f.items():
                            content += key + ': ' + val + '\n'

        return content

def setup(bot):
    bot.add_cog(MsgBlock(bot))
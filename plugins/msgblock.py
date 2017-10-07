import discord
from discord.ext import commands
from ruamel import yaml
import re

class MsgBlock:
    def __init__(self, bot):
        self.bot = bot
        self.dependancy = ["settings"]
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
        if msg.guild.id == 111504456838819840 and msg.channel.id != 270033143996612608:
            if not any(e in [r.id for r in msg.author.roles] for e in self.roles):
                # Invte detection
                inv = self.discord_re.findall(self._embed_extractor(msg))
                if inv:
                    for l, i in inv:
                        try:
                            a = await self.bot.get_invite(i)
                            if a.guild.id not in self.bypass_server:
                                await msg.delete()
                                await msg.channel.send(
                                    "{}'s message has been deleted due to: contains an unauthorized invite link.".format(
                                        msg.author.mention))

                                c = self.bot.get_channel(328507346655641601)
                                em = discord.Embed(colour=discord.Colour(value=None).orange())

                                if msg.author.avatar_url is not None:
                                    em.set_author(name=str(msg.author), icon_url=msg.author.avatar_url)
                                else:
                                    em.set_author(name=str(msg.author), icon_url=msg.author.default_avatar_url)
                                em.add_field(name="Content", value=msg.content, inline=False)
                                em.add_field(name="User ID", value=msg.author.id)
                                em.add_field(name="Message ID", value=msg.id)
                                em.add_field(name="Posted at", value=msg.channel.name)

                                await c.send(embed=em)
                        except (discord.NotFound, discord.HTTPException):
                            pass # We don't really need it

                # Mention spamming detection
                if msg.mentions:
                    if len(msg.raw_mentions) > 5 or len(msg.raw_role_mentions) > 3:
                        await msg.author.ban(
                            reason="[ROTOM] Mass ping detected, see #d-rotom_logs for details.")

                        await msg.channel.send(
                            "{} has been banned due to: mass pings.".format(
                                msg.author.mention))

                        c = self.bot.get_channel(328507346655641601)
                        em = discord.Embed(colour=discord.Colour(value=None).red())

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


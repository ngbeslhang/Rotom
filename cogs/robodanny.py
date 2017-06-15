"""Google command copied from RoboDanny at https://github.com/Rapptz/RoboDanny/blob/53a3e202db197c2149811af9f555d5a6db638236/cogs/buttons.py#L292

WARNING: ONLY WORKS WITH ASYNC/LEGACY VERSION OF DISCORD.PY (NOT MODIFIED TO WORK WITH REWRITE)"""
from discord.ext import commands
import discord
import aiohttp
from lxml import etree
from urllib.parse import parse_qs


class RoboDanny:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['google'])
    async def g(self, *, query):
        """Searches google and gives you top result."""
        try:
            card, entries = await self.get_google_entries(query)
        except RuntimeError as e:
            await self.bot.say(str(e))
        else:
            if card:
                value = '\n'.join(entries[:3])
                if value:
                    card.add_field(name='Search Results', value=value, inline=False)
                return await self.bot.say(embed=card)

            if len(entries) == 0:
                return await self.bot.say('No results found... sorry.')

            next_two = entries[1:3]
            first_entry = entries[0]
            if first_entry[-1] == ')':
                first_entry = first_entry[:-1] + '%29'

            if next_two:
                formatted = '\n'.join(map(lambda x: '<%s>' % x, next_two))
                msg = '{}\n\n**See also:**\n{}'.format(first_entry, formatted)
            else:
                msg = first_entry

            await self.bot.say(msg)
            await self.bot.say("*Credits to Rapptz for command source code: <https://github.com/Rapptz/RoboDanny/>*")

    async def get_google_entries(self, query):
        params = {
            'q': query,
            'safe': 'on',
            'lr': 'lang_en',
            'hl': 'en'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
        }

        # list of URLs
        entries = []

        # the result of a google card, an embed
        card = None

        async with aiohttp.get('https://www.google.com/search', params=params, headers=headers) as resp:
            if resp.status != 200:
                raise RuntimeError('Google somehow failed to respond.')

            root = etree.fromstring(await resp.text(), etree.HTMLParser())

            # with open('google.html', 'w', encoding='utf-8') as f:
            #     f.write(etree.tostring(root, pretty_print=True).decode('utf-8'))

            """
            Tree looks like this.. sort of..
            <div class="g">
                ...
                <h3>
                    <a href="/url?q=<url>" ...>title</a>
                </h3>
                ...
                <span class="st">
                    <span class="f">date here</span>
                    summary here, can contain <em>tag</em>
                </span>
            </div>
            """

            card_node = root.find(".//div[@id='topstuff']")
            card = self.parse_google_card(card_node)

            search_nodes = root.findall(".//div[@class='g']")
            for node in search_nodes:
                url_node = node.find('.//h3/a')
                if url_node is None:
                    continue

                url = url_node.attrib['href']
                if not url.startswith('/url?'):
                    continue

                url = parse_qs(url[5:])['q'][0] # get the URL from ?q query string

                # if I ever cared about the description, this is how
                entries.append(url)

                # short = node.find(".//span[@class='st']")
                # if short is None:
                #     entries.append((url, ''))
                # else:
                #     text = ''.join(short.itertext())
                #     entries.append((url, text.replace('...', '')))

        return card, entries
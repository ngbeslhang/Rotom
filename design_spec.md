***NOTE***: Everything here should be considered as self-notes, however suggestions are recommended.
## Language pack implementation
A cog must be able to use the language system like this:

```py
from discord.ext import commands

class Cog:
    def __init__(self, bot):
        self.bot = bot
        self.lang = self.bot.get_lang('cmd_cog')

    @commands.command(pass_context=True)
    def quak_quak(self, ctx):
        self.bot.say(self.lang.get('quak.reply', ctx))
```
- `Bot.get_lang()` **MUST** return a class
- ...whose get() can be called to fetch requested string from the language pack

The returned class of `Bot.get_lang()` **MUST**:
- have a required param `filename` in `__init__()`
- consist of `get()` function
- have a local dictionary for YAML with the passed `filename` in each language pack
  - if unable to find any, set it as `None` instead
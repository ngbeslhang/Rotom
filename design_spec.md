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
- have a required param `filename` and `path_obj` in `__init__()`
- consist of `get()` function
- have a local dictionary for YAML with the passed `filename` in each language pack
  - if unable to find any, set it as `None` instead

***OR***

Example translation file:
```
"Hello, world!": "您好世界"
```
In Python:
```py
print(locale('Hello, world!', 'zh_cn'))
```

There should be no need for __info__.yaml, considering removing it

## Guild-based settings tree (in database)
```
server_id
|- superadmin: array (either role or member ID)
|- moderator: array (either role or member ID)
```
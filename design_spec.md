***NOTE***: Everything here should be considered as self-notes, however suggestions are welcomed.
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
- consist of `reload()` function
- have a local dictionary for YAML with the passed `filename` in each language pack
  - if unable to find any, set it as `None` instead

***OR***

Example translation file:
```yaml
"Hello, world!": "您好世界"
```
In Python:
```py
print(locale('Hello, world!', 'zh_cn'))
```


There should be no need for __info__.yaml, considering removing it
***OR***

Write a custom Bot.say() & inherited Embed class instead that checks message author's language preference (via database).
Example translation file:
```yaml
"Hello, world!":     # The key itself would be considered as "en_us"
  zh_cn: "你好，世界！"
```
Fetching translated string is as easy as:
```py
self.bot.say("Hello, world!") # replies with 你好，世界！" if user's lang pref is zh_cn

# pass say() translate param if you don't want it to be automatically translated.
self.bot.say("Hello, world!", translate=False) # Can be easily replaced with Ctrl+F'ing "translate=False"


```

## Guild-based settings tree (in database)
```
server_id
|- superadmin: array (either role or member ID)
|- moderator: array (either role or member ID)
```
***NOTE***: Everything here should be considered as self-notes, however suggestions are welcomed.
## `tldlist` command
- Now that https://tld-list.com has updated their UI and introduced domain availability search I could scrap the site and create a command using the data.
  - Aliases: `tld`, `domain`

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

Write a custom Bot.say(), other relevant functions & inherited Embed class instead that checks message author's language preference (via database).
Example translation file:
```yaml
"Hello, world!":     # The key itself would be considered as "en_us"
  zh_cn: "你好，世界！"
```
Fetching translated string is as easy as:
```py
self.bot.say("Hello, world!") # replies with 你好，世界！" if user's lang pref is zh_cn

# pass say() translate param if you don't want it to be automatically translated.
self.bot.say("Hello, world!", translate=False) # Can be easily replaced with Ctrl+F'ing "translate=False" if you want to use cogs that contains this on other bots

# lang param will be required if there's no database module loaded

```

## Object tree (in database)
```
id
|- type "server"
|-- superuser: array (either role or member ID, server owner's ID included)
|-- admin: array (either role or member ID)
```
**NOTE**: Bot owner(s), by default, is a superuser of *all servers the bot is in* so the bot owner(s) will be able to provide support to any servers using their bot.

**NOTE**: Superuser and admin WILL BE ENTIRELY SEPARATE. Superuser cannot perform any adminstration commands while admin can. 
- But let's be honest that could be bypassed with built-in eval command anyway, and it's an essential command for bot support, which means a certain trust between the bot owner(s) and the server owner(s) is **needed**. The eval command will log who and what code did said person run.

## Database specs
Malena and Liara's suggestion: `table.get(key)` which means creating a new table class

# Music
## Auto Pause/Unpause
~~Definitely not~~ Inspired by HcgRandon's Ayana.
- Pause the current song and list when there's no listeners (aka non-bots) in the VC for minutes (able to set via config file)

## `play/add` Command
- Usage: `play/add <link/tag> [from time/start|till time/end|from time/start till time/end (in MM:SS format) ]`
  - Example: `play BRAIN POWER from 1:00 till end` or `play BRAIN POWER from 1:00` assuming that `BRAIN POWER` is a tag 
- Supports YouTube/SoundCloud/Twitch
- Supports playing from/until a time/ within the period


## `song` Command
- Only the requester, superusers/admins (user/roles) and bot owner can control the current song.
  - To prevent infinite loop abuse, the superusers/admins (user/roles) can set how many times can a song repeat/restart/goto
    - By default unless they are specifically specified as infinite, if only one was set the value applies to the rest as well
      - This also applies to how many times can the same link get added into the queue.
    -  If majority of the listeners in a server wanted to repeat a song infinitely it's already remedied by local-storage system 
- `play`
- `pause`
- `restart`
- `goto <time (in MM:SS format)>`
- `repeat`

## `skip` Command
- Skips either the current song, the `playlist` (if it was requested) or `queue`

## `queue` command
- `repeat`
- `shuffle`

## Music local-storage system
**NOTE**: A way to prevent getting IP banned by YouTube for scraping too much.
- Either store it locally or fetch the files from other servers

## Tags system (`get`, `set`, `give`, `remove` and `block` command groups)
- `role`
  - SET (e.g. `set role <role tag>`)
    - At this point it requires a multiline codeblock in YAML config for settings and will be loaded with YAML parser.
      - In a way JSON is also supported since YAML parser is also technically a JSON parser.
      - `safe_load()` will be used.
      - Format:
        ```yaml
        <tag>:
          who_can_get:

        ```
        Example:
        ```yaml
        mature:
        ```
  - GET (e.g. `get role <role tag>`)
- `info` (in a way replaces `userinfo`)
  - Aliases: `info from`, `details`, `details from`
  - GET (e.g. `get info from <object>`)
    - User/channel/role name/ID/mention
      - For name search:
        - User: the default choice, but for the sake of it, `u:` or `user:` prefix, case-insensitive
        - Channel: add a `c:` or `channel:` prefix, case-insensitive
        - Role: add a `r:` or `role:` prefix, case-insensitive
    - `server`
    - `bot`
- `setting`
  - Aliases: `settings`
  - GET (e.g. `get setting from <tag>`)
    - Aliases: `setting from`, `settings from`
  - SET (e.g. `set settings of <tag>`)
    - Aliases: `setting of`, `settings of`
- Generic tags

**NOTE**: Unless specified otherwise, if a tag type isn't mentioned in the subcommand it means it's not usable for said type.

## `load` and `unload` bot-owner command groups
- `cog/cogs`
  - Supports multiple cog names at once, separated by space
- `lang/language`
  - Supports multiple lang names at once, separated by space

## API
- Pretty much essential for multiserver communication (for region-based music playing mainly)

## Annnnd other people's requests
- https://owo.whats-th.is/ce77f8.png https://owo.whats-th.is/bbc4ac.png (okay not too shabby actually)
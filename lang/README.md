# Localization
Rotom relies on localization files for all command outputs.

# Specification (Skip if you just want to translate)
- ALL top level keys are RECOMMENDED not to exceed one/two levels of nestings.

## Adding multilanguage support to cogs
A cog must have a variable assigned to the returned value of Rotom's `Bot.get_lang()`, which will be a class that contains `get()` for you to get strings you need.
1. Assign `bot.get_lang()` (read the function's docstring for usage) to an attribute in the cog's `__init__()`.
2. When needed, call said attribute's `get()` function

Example:
```py
class Cog:
    def __init__(self, bot):
        self.bot = bot
        self._lang = bot.get_lang('cmd_cog')
        self.l = self._lang.get # Optional, just to make things easier

    def print(self):
        print(self.l('quak quak', 'en_us'))
```

## Adding your translation into official repo
Please contact me via Discord (ngb#0995) along with a link to your translation.
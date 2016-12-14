# Langauge pack
Language packs, as the name implies, is the essential part of Rotom's multilanguage system, which Rotom (including it's logging system) depends on.
The source code of Rotom itself doesn't have any hardcoded strings (beside docstrings), instead it gets the strings it need from the language packs.

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

## Adding your language pack into official repo
1. You can contact me via Discord (ngb#0995) along with a link to your language pack.
2. I'll check the folder for any inconsistency and will correct them if found.
3. Once contacted I will contact anyone I trust (who also knows the pack's language well) to verify it's accuracy and validity.
  - If there's any inaccuracies et cetera in your translations AND if said validators corrected it, he/she/they WILL be added into the author list if they want to.
4. After the pack is verified, your pack will be added to official git repo (i.e. here), you'll be credited for creating the pack and you'll get a Translator role at Rotom's support Discord server.
  - You might be contacted (mainly by Discord) to translate new strings from either Rotom or any other possible projects I've started (you can choose not to participate the latter).

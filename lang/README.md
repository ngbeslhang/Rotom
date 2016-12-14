# Langauge pack
**NOTE**: "pack" in this README is a shortform of "language pack" and it will be used extensively.

Language packs, as the name implies, is the critical part of Rotom's multilanguage system, which means Rotom will **NOT** work without the packs, since even the logging system uses it.
Rotom itself doesn't use any hardcoded strings (beside docstrings), instead it gets the strings from the language packs.

## Adding multilanguage support to cogs
A cog must have a variable assigned to the returned value of Rotom's `Bot.get_lang()`, which will be a class that contains `get()` for you to get strings you need.
*More info regarding how the bot imports the YAML file for use*

Things you can search for in a language pack:
- Command description
- Reply string
- Log string
- and more I probably am unaware of

## Adding your language pack into official repo
**NOTE**: Natural and natural languages ONLY.

1. You can contact me via Discord (ngb#0995) along with a link to your language pack.
2. I'll check both the folder's name and the `__info__.yaml`.
  - If the folder name isn't in ISO 639-1 format, it wil be renamed to corresponding code.
  - If the `name` and/or `author` in `__info__.yaml` aren't formal (e.g. not capitalized) either or both will be modified to make it look as formal as possible.
3. Once contacted I will contact anyone I trust (who also knows the pack's language well) to verify it's accuracy and validity.
4. After the pack is verified, your pack will be added to official repo (i.e. here), you'll be credited for creating the pack and you'll get a Translator role at Rotom's support Discord server.
  - You might be contacted (mainly by Discord) to translate new strings from either Rotom or any other possible projects I've started (you can choose not to participate the latter).


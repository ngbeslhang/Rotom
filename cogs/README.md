# Extensions (cogs)
Rotom supports all cogs written with rewrite version of `discord.py`'s* command extension, but:
- Support both async and rewrite version of `discord.py`
- Use Rotom's non-standard* features
- No guarantee that they will be supported by Rotom out-of-the-box...
  - ... which means they *might* require modification to work with Rotom.

* ...as long as it's vanilla (unmodified)

## Writing extensions
**NOTE**: Everything under this section, including the sub-sections, should support other bots written in `discord.py`'s `command` extension unless Rotom's non-standard features were used.

### Configuration
All cogs' setttings can be set as a global key with the cog name as the key name (more in config_template.yml), and there is a special helper called `rotom.Bot.get_conf`.

The returned object will be under `dict` type. BUNCH might probably be considered to replace it instead.

### Multi-file extensions
There's two officially-supported ways (there might be other ways but yet to be confirmed) to write an extension that contain multiple files.
- `__init__.py` inside the folder (recommended)
- create an external `.py` file then load contents from a designated folder

### Dependencies
There's two ways to check for dependencies if your extension requires other extension(s) in order to work.
- Check for attribute that's unique to the cog.
- Check if said cog is imported

### Warning for writing database extensions
If your database extension will set a `db` attribute to `rotom.Bot` instance on load:
- It must have the **EXACT** interfaces incl. the exceptions as `db_rethinkdb` (`select()`, `write()`, `delete()`, `_eval()`)
- If the bot's unable to connect to the database the `db` attribute must **NOT** be set

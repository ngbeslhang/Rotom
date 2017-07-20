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
Refer to `cogs` folder -> `cog_website` folder and `website.py`.

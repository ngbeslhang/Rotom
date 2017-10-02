# Rotom
**NOTE:** This repo is still WIP.

# Requirement
- Python 3.5 / 3.4 (former is recommended)
  - `discord.py`

# Installation
WIP

# Configuration
A template config file is provided for you to start with.
**WARNING:** You are expected to have a minimal basic understanding of Python or programming in general.

```yaml
# If unsure, Google the term + "YAML" without quotes
---
bot:
  # Your bot's token
  token: quakquakquak

  # Your bot's prefix
  prefix: r.
  # Supports either a string like the one above or a list/array/collection:
  #   prefix: 
  #     - r.
  #     - bzzt

  # Bypass all bots' messages so they won't be able to used this bot's commands
  bypass_bot_messages: yes/no

  plugins:
    # Directory of plugins, both relative and absolute are supported
    dir: plugins

    # Choose what plugins to load while the bot is starting
    load: ~
    # Enter ~ to disable plugin loading, otherwise the same as prefix config

  # Read the parameters section of the link below...
  # http://discordpy.readthedocs.io/en/rewrite/api.html#discord.Client
  # ...and check everything ABOVE the add_check() for a complete list of params:
  # http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#discord.ext.commands.Bot.add_check
  # (ignore all command_prefix and formatter)
  params: ~
  # When needed, do it like this:
  #   params:
  #     description: An ever evolving bot.
  #     self_bot: no
```

If config for the plugins are needed, put the configs right under the `bot` and so on:
```yaml
---
bot:
  token: TOKEN
  prefix: r.
  bypass_bot_messages: yes

  plugins:
    dir: plugins
    load: adblock

  params: ~

# Below is a plugin config example
adblock:
    block: 
      - discord.gg/*
    bypass:
      - discord.gg/pokemon
````
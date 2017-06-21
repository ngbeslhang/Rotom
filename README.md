# Rotom

**WARNING:** **DO NOT** edit .gitignore UNLESS you know what are you doing.

**NOTE:** This repo is still WIP.

Rotom is an ever-evolving Discord bot designed with modularity in mind.

## TODO

- Remove `api` section from `config_template.yml` and follow the way RoboDanny implemented Carbonitex (`api` folder in cogs)

## Requirement

- Python 3.5+
- RethinkDB

### Modules

- rewrite branch of `discord.py`
- `ruamel.yaml`

## Installation

**NOTE**: WIP

## Extensions (cogs)
Rotom supports all cogs written for discord.py, but there's no guarantee that every extrensions will:
- Support both async and rewrite version of `discord.py`
- Use Rotom's non-standard features
- Supporting Rotom at all (due to possible usage of other bots' non-standard features)
**NOTE**: By non-standard I mean anything that's not officially included inside discord.py (and usually written by third-party)

### Writing extensions
**NOTE**: Everything under this section, including the sub-sections, should support other bots written in `discord.py`'s `command` extension unless Rotom's non-standard features were used.

TBD
#### Multi-file extensions
Refer to `cogs` folder -> `cog_website` folder and `website.py`.

## Special thanks

**NOTE**: Unless otherwise requested not to, anyone who helped me and/or contributed in any way will be added to here.

- Discord API guild's #python_discord-py regulars for helping and teaching me in numerous ways.
- [Rapptz](https://github.com/Rapptz) for creating discord.py + its fantastic `ext.commands` extension and [Robo Danny's source code](https://github.com/Rapptz/RoboDanny).
- [SunDwarf](https://github.com/SunDwarf) for his private musicbot source code (used as reference for Rotom's music cog).
- [Thessia](https://github.com/Thessia) for (letting me shamelessly copy) [his bot's source code](https://github.com/Thessia/Liara).
- [HcgRandon](https://github.com/hcgrandon) for providing inspirations for Rotom's music cog.

(*) Don't worry, all links here are GitHub's.

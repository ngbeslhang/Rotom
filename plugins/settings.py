from discord.ext import commands

class Settings:
    """A settings dependancy for other plugins."""

    @commands.command(hidden=True)
    async def settings(self, ctx, *, code):
        # remove ```\n```, shamelessly copied from robodanno
        if code[-3:] == "```":
            split = code.split('\n')
            split[-1] = split[-1].split('```')[0]
            split.append('```')
            code = '\n'.join(split)

        if code.startswith('```') and code.endswith('```'):
            code = '\n'.join(code.split('\n')[1:-1])
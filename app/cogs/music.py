from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
import config

print(config.GUILD_IDS)

# example cog
class Slash(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="test", guild_ids=config.GUILD_IDS)
    async def _test(self, ctx: SlashContext):
        embed = Embed(title="Embed Test")
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Slash(bot))

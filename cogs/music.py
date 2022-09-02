from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("getting playlist")

        cursor = self.bot.db_session.client.roosterbot.playlist.find()
        print(await cursor.to_list(length=100))


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))

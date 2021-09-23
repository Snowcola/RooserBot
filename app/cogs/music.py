from discord import Embed, VoiceChannel, VoiceClient
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
import discord.utils
import config

config.logger.info(f"Slash commands configured for Guild-IDs: {config.GUILD_IDS}")

# example cog
class Slash(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.channel: VoiceChannel = None

    def check_connected(self, ctx):
        voice_client: VoiceClient = discord.utils.get(
            ctx.bot.voice_clients, guild=ctx.guild
        )
        return voice_client and voice_client.is_connected()

    @cog_ext.cog_slash(
        name="join",
        guild_ids=config.GUILD_IDS,
        description=f"Ask RoosterBot to join you in a voice channel",
    )
    async def _join(self, ctx: SlashContext):
        try:
            join_channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.reply("you are not in a voice channel")
            return
        if self.channel == join_channel:
            await ctx.reply(f"{self.bot.user.name} is already in **{join_channel}**")
            return
        await join_channel.connect()
        self.channel = join_channel
        await ctx.send(f"{self.bot.user.name} has joined **{join_channel}** ")

    @cog_ext.cog_slash(
        name="leave",
        guild_ids=config.GUILD_IDS,
        description=f"Ask RoosterBot to leave the voice channel",
    )
    async def _leave(self, ctx: SlashContext):
        if self.check_connected(ctx):
            await ctx.guild.voice_client.disconnect()
            await ctx.reply("Goodbye!")
            self.channel = None
        else:
            await ctx.reply(f"{self.bot.user.name} is not in a voice channel")

    @cog_ext.cog_slash(
        name="add song",
        guild_ids=config.GUILD_IDS,
        description=f"Add a song to the playlist",
        options={
            "name": "song",
            "description": "the song you want to add to the playlist",
            "type": 3,
            "required": True,
        },
    )
    async def _add_song(self, ctx: SlashContext, song: str):
        await ctx.reply(f"adding {song} to playlist")


def setup(bot: Bot):
    bot.add_cog(Slash(bot))

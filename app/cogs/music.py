import asyncio
from dataclasses import dataclass
from operator import mul
import typing
from discord import Embed, VoiceChannel, VoiceClient, FFmpegOpusAudio, FFmpegPCMAudio
from discord.ext.commands import Bot, Cog
from typing import Union
from discord_slash import cog_ext, SlashContext
import discord.utils
import config
from collections import deque
from youtube_dl import YoutubeDL
from datetime import timedelta


@dataclass
class Song:
    title: str
    source: str
    thumbnail: str
    web_url: str
    duration: int
    _embed: Union[Embed, None] = None

    @property
    def embed(self):
        if not self._embed:
            embed = Embed(title=self.title, url=self.web_url)
            embed.set_thumbnail(url=self.thumbnail)
            embed.add_field(name="Length", value=self.duration_time)
            self._embed = embed
        return self._embed

    @property
    def duration_time(self):
        duration = {}
        duration["hours"], rem = divmod(self.duration, 3600)
        duration["minutes"], duration["seconds"] = divmod(rem, 60)
        if duration["hours"] > 0:
            return f"{duration['hours']:02}:{duration['minutes']:02}:{duration['seconds']:02}"
        return f"{duration['minutes']:02}:{duration['seconds']:02}"


# example cog
class Music(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.channel: VoiceChannel = None
        self.voice_client: VoiceClient = None
        self.is_playing = False

        # consder db support so playlist can survive restarts
        self.music_queue: typing.Deque[Song] = deque()

        self.YTDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
        self.FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }

    def is_playing(self):
        return self.voice_client and self.voice_client.is_playing()

    def is_paused(self):
        return self.voice_client and self.voice_client.is_paused()

    def check_connected(self, ctx):
        voice_client: VoiceClient = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    def update_voice_state(self, ctx):
        voice_client: VoiceClient = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client:
            self.voice_client = voice_client
            self.channel = voice_client.channel

    @cog_ext.cog_slash(
        name="join",
        guild_ids=config.GUILD_IDS,
        description=f"Ask RoosterBot to join you in a voice channel",
    )
    async def _join(self, ctx: SlashContext) -> typing.Union[bool, None]:
        await self.join(ctx)

    async def join(self, ctx: SlashContext):
        self.update_voice_state(ctx)
        try:
            join_channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.reply("you are not in a voice channel")
            return False
        print("{self.channel=} {join_channel=}")
        if self.channel and self.channel.id == join_channel.id:
            await ctx.reply(f"{self.bot.user.name} is already in **{join_channel}**")
            return
        await join_channel.connect()
        self.channel = join_channel
        self.voice_client = ctx.guild.voice_client
        await ctx.reply(f"{self.bot.user.name} has joined **{join_channel}** ")

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
        name="add",
        description=f"Add a song to the playlist",
        options=[
            {
                "name": "song",
                "description": "the song you want to add to the playlist",
                "type": 3,
                "required": True,
            },
        ],
    )
    async def _add(self, ctx: SlashContext, song: str):
        await ctx.defer()
        if song_result := self.search_youtube(song)[0]:
            self.music_queue.append(song_result)
            song_result.embed.set_footer(text=f"Added by {ctx.author.nick}", icon_url=ctx.author.avatar_url)
            song_result.embed.color = discord.Color.green()
            await ctx.send(f":white_check_mark:  **{song_result.title}** successfully added!", embed=song_result.embed)

            return
        await ctx.reply(f":x:  **{song}** could not be found: ")

    @cog_ext.cog_slash(
        name="playlist",
        description=f"List songs in the playlist",
    )
    async def _playlist(self, ctx: SlashContext):
        embed = Embed(title=f"Playlist ({len(self.music_queue)} tracks)", color=discord.Color.purple())
        track_list = []
        for idx, track in enumerate(self.music_queue):
            track_list.append(f"`{idx+1}` [{track.title}]({track.web_url}) {track.duration_time}")
        if track_list:
            embed.description = "\n".join(track_list)
        await ctx.reply(embed=embed)

    def search_youtube(self, song: str, multiple=False, max_entries=10) -> Union[list[Song], bool]:
        with YoutubeDL(self.YTDL_OPTIONS) as ytdl:
            try:
                results = ytdl.extract_info(f"ytsearch:{song}", download=False)["entries"]
                info = results[0]
            except Exception:
                return False
        if multiple:
            song_results = []
            for song in results[: min(len(results), max_entries)]:
                song_results.append(
                    Song(
                        source=info["formats"][0]["url"],
                        title=info["title"],
                        thumbnail=info["thumbnails"][1]["url"],
                        web_url=info["webpage_url"],
                        duration=info["duration"],
                    )
                )
            return song_results

        return [
            Song(
                source=info["formats"][0]["url"],
                title=info["title"],
                thumbnail=info["thumbnails"][1]["url"],
                web_url=info["webpage_url"],
                duration=info["duration"],
            )
        ]

    @cog_ext.cog_slash(
        name="play",
        description=f"Start playing from the playlist",
    )
    async def _play(self, ctx: SlashContext):
        if not self.check_connected(ctx):
            can_join = await self.join(ctx)
            if can_join == False:
                ctx.reply("Please join a voice channel first")
                return
        if len(self.music_queue) > 0:
            await ctx.reply(f"**Now Playing**", embed=self.music_queue[0].embed)
            self.play_next()
        else:
            await ctx.reply(f"I don't have any songs to play, please add one first")

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            track = self.music_queue.popleft()

            self.voice_client.play(
                FFmpegPCMAudio(track.source, **self.FFMPEG_OPTIONS), after=lambda x: self.play_next()
            )
        else:
            self.is_playing = False

    ## Stop

    ## Skip

    ## Volume


def setup(bot: Bot):
    bot.add_cog(Music(bot))

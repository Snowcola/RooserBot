from discord.ext.commands import Cog, Bot
from discord_slash import cog_ext, SlashContext, ComponentContext
from typing import Optional, Deque
from collections import deque

from cogs import MusicPlayer, Song, YoutubeSearch


class PlaylistManager(Cog):
    def __init__(self, bot: Bot, player: MusicPlayer) -> None:
        self.bot: Bot = bot
        self.player = player

    @cog_ext.cog_slash(name="add-playlist", options=[{"name": "playlist_url", "type": 3}])
    async def _add_playlist(self, ctx: SlashContext, playlist_url: Optional[str] = None) -> None:
        await ctx.defer()
        results = YoutubeSearch.search_playlist(playlist_url, ctx)
        self.player.music_queue.extend(results)
        # button is this the playlist you want to add?
        await ctx.reply(f"Added playlist: {playlist_url}", embed=self.player.playlist_embed())

    @cog_ext.cog_subcommand(base="playlist", name="clear")
    async def _playlist_clear(self, ctx: SlashContext) -> None:
        self.player.music_queue = deque()
        await ctx.reply(":white_check_mark: Playlist Cleared", embed=self.player.playlist_embed())

import asyncio
from asyncio.locks import Event
from asyncio.tasks import sleep
from enum import Enum, auto
from logging import LoggerAdapter
from typing import Optional
import discord
from discord.ext.commands import Cog, Bot
from discord.guild import Guild
from discord_slash import SlashContext, ButtonStyle, ComponentContext, cog_ext
from discord_slash.utils.manage_components import create_button, create_actionrow
import cogs

from config import logger
from discord import Color, Embed, embeds, widget


class PlayState(Enum):
    STOPPED = auto()
    PLAYING = auto()
    PAUSED = auto()

    def readable(val):
        val_map = {
            PlayState.STOPPED: "⏹ stopped",
            PlayState.PLAYING: "▶️ playing",
            PlayState.PAUSED: "⏸️ paused",
        }
        return val_map[val]


class PlayerWidget(Cog):
    def __init__(self, bot: Bot, music_player: cogs.MusicPlayer) -> None:
        self.bot = bot
        self.player = music_player
        self.current_message = None
        self.asset_guild: Optional[Guild] = None

    @Cog.listener()
    async def on_connect(self):
        await asyncio.sleep(5)
        self.asset_guild: Guild = self.bot.get_guild(220318911818760192)
        self.emojis = {x.name: x for x in self.asset_guild.emojis}
        logger.debug(f"{self.asset_guild=}")
        logger.debug(f"{self.emojis=}")

    def playing_status(self):
        play_status = PlayState.STOPPED
        if self.player.is_stopped:
            play_status = PlayState.STOPPED
        if self.player.is_playing and self.player.is_paused:
            play_status = PlayState.PAUSED
        if self.player.is_playing and not self.player.is_paused:
            play_status = PlayState.PLAYING
        return play_status

    def create_play_button(self) -> dict:
        display = {
            PlayState.STOPPED: {"style": ButtonStyle.green, "emoji": self.emojis["play"]},
            PlayState.PAUSED: {"style": ButtonStyle.green, "emoji": self.emojis["play"]},
            PlayState.PLAYING: {"style": ButtonStyle.blurple, "emoji": self.emojis["pause"]},
        }

        play_state = self.playing_status()

        button = create_button(label="", custom_id="button_play_pause", **display[play_state])
        return button

    def create_stop_button(self):
        disabled = self.playing_status() == PlayState.STOPPED
        button = create_button(
            style=ButtonStyle.red, emoji=self.emojis["stop"], label="", custom_id="button_stop", disabled=disabled
        )
        return button

    def create_embed(self):
        play_state = self.playing_status()
        embed_color = {PlayState.STOPPED: Color.red(), PlayState.PAUSED: Color.teal(), PlayState.PLAYING: Color.green()}
        embed = Embed(title=f"Rooster Player", color=embed_color[play_state])
        # embed.set_footer(text=f"{PlayState.readable(play_state)}")
        if self.player.now_playing.duration > 0:
            embed.set_thumbnail(url=self.player.now_playing.thumbnail)
            embed.add_field(name="Now Playing", value=self.player.now_playing.title, inline=False)
            embed.add_field(name="Volume", value=f"{self.player.volume*100:.0f}%")
        else:
            embed.add_field(name="Now Playing", value="stopped", inline=False)
            embed.add_field(name="Volume", value=f"{self.player.volume*100:.0f}%")
        ## need to validate length
        if len(self.player.music_queue) > 0:
            embed.add_field(name="Next Up", value=self.player.music_queue[0].title, inline=False)
        else:
            embed.add_field(name="Next Up", value="playlist empty", inline=False)

        return embed

    def prepare_widget(self):
        return dict(components=self.create_player_widget_actions(), embed=self.create_embed())

    async def update(self, defer=0):
        widget = self.prepare_widget()
        if defer:
            await asyncio.sleep(defer)
        await self.current_message.edit(**widget)

    async def show(self, ctx: SlashContext):
        widget = self.prepare_widget()
        msg = await ctx.channel.send(**widget)
        self.current_message = msg

    def create_player_widget_actions(self):
        play_pause = self.create_play_button()
        stop = self.create_stop_button()
        skip = create_button(
            style=ButtonStyle.primary,
            label="",
            emoji=self.emojis["next"],
            custom_id="button_skip",
            disabled=self.playing_status() == PlayState.STOPPED,
        )
        volume_up = create_button(
            style=ButtonStyle.blurple,
            label="",
            emoji=self.emojis["volume_up"],
            custom_id="button_volume_up",
            disabled=self.player.volume == 100,
        )
        volume_down = create_button(
            style=ButtonStyle.blurple,
            label="",
            emoji=self.emojis["volume_down"],
            custom_id="button_volume_down",
            disabled=self.player.volume == 0,
        )
        action_row = create_actionrow(play_pause, stop, skip, volume_down, volume_up)
        return [action_row]

    @cog_ext.cog_component()
    async def button_stop(self, ctx: ComponentContext):
        logger.debug(f"Stopping from widget")
        self.player.stop()
        await ctx.edit_origin(**self.prepare_widget())

    @cog_ext.cog_component()
    async def button_skip(self, ctx: ComponentContext):
        logger.debug(f"Skipping from widget")
        await self.player.skip(ctx, silent=True)
        await ctx.edit_origin(**self.prepare_widget())
        await self.update(defer=6)

    @cog_ext.cog_component()
    async def button_play_pause(self, ctx: ComponentContext):
        await ctx.defer(edit_origin=True)
        state = self.playing_status()
        if state == PlayState.PLAYING or state == PlayState.PAUSED:
            logger.debug(f"Pause/Resume from widget")
            self.player.pause_resume()
        else:
            logger.debug(f"Playing from widget")
            await self.player.play(ctx, silent=True)
        await ctx.edit_origin(**self.prepare_widget())

    @cog_ext.cog_component()
    async def button_volume_up(self, ctx: ComponentContext):
        current_volume = self.player.get_volume()
        logger.debug(f"Volume up to: {current_volume+10}")
        self.player.set_volume(current_volume + 10)
        await ctx.edit_origin(**self.prepare_widget())

    @cog_ext.cog_component()
    async def button_volume_down(self, ctx: ComponentContext):
        current_volume = self.player.get_volume()
        logger.debug(f"Volume down to: {current_volume-10}")
        self.player.set_volume(current_volume - 10)
        await ctx.edit_origin(**self.prepare_widget())
        logger.debug(ctx.guild_id)
        logger.debug(ctx.guild.id)

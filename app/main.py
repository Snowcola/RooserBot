import os
from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from utils.cogs import load_available_cogs
import config

bot = Bot(command_prefix="!", self_bot=True, intents=Intents.default())
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print(f"{bot.user.name} connected")


load_available_cogs(bot)

bot.run(config.DISCORD_TOKEN)

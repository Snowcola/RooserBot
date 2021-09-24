import argparse

from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand

import config
from config import logger
from utils.cogs import load_available_cogs

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sync-commands", dest="sync", action="store_true")
args = parser.parse_args()

bot = Bot(command_prefix="!", self_bot=True, intents=Intents.default())
logger.info(f"{'not s' if args.sync else 'S'}yncing commands with Discord")
slash = SlashCommand(bot, sync_commands=args.sync)


@bot.event
async def on_ready():
    logger.info(f"{bot.user.name} connected")


load_available_cogs(bot)

bot.run(config.DISCORD_TOKEN)

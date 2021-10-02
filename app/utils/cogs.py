from pathlib import Path
from discord.ext.commands import Bot
from config import logger, DEV


def load_available_cogs(bot: Bot):
    cog_location = Path("./app/cogs") if DEV else Path("/app/cogs")
    logger.debug(f"Looking for cogs at {cog_location}")
    files = [x for x in cog_location.glob("*_cog.py")]
    logger.info(f"loading cogs {[str(file) for file in files]}")

    for file in files:
        cog = file.stem
        dir = str(file.parents[0]).split("/")[-1]
        logger.debug(f"Loading cog: {cog}")
        bot.load_extension(f"{dir}.{cog}")

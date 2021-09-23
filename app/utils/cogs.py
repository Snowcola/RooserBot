from pathlib import Path
from discord.ext.commands import Bot
from config import logger


def load_available_cogs(bot: Bot):
    files = [x for x in Path("./app/cogs").glob("*.py") if "__init__" not in str(x)]
    logger.info(f"loading cogs {[str(file) for file in files]}")

    for file in files:
        cog = file.stem
        dir = str(file.parents[0]).split("/")[-1]
        logger.debug(f"Loading cog: {cog}")
        bot.load_extension(f"{dir}.{cog}")

import os
import logging

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename="/app/logs/discord.log", encoding="utf-8", mode="w"
)
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

GUILD_IDS = [220318911818760192]
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

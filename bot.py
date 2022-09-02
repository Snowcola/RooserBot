import asyncio
import logging
import logging.handlers
import os

from typing import List, Optional

import motor.motor_asyncio as db
import discord
from discord.ext import commands

# from aiohttp import ClientSession
from dotenv import load_dotenv


class RoosterBot(commands.Bot):
    """Rooster Bot"""

    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        db_session: db.AsyncIOMotorClientSession,
        # web_client: ClientSession,
        testing_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.db_session = db_session
        # self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:

        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.

        for extension in self.initial_extensions:
            await self.load_extension(extension)
            print(f"{extension} successfully loaded")

        # In overriding setup hook,
        # we can do things that require a bot prior to starting to process events from the websocket.
        # In this case, we are using this to ensure that once we are connected, we sync for the testing guild.
        # You should not do this for every guild or for global sync, those should only be synced when changes happen.
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            # We'll copy in the global commands to test with:
            self.tree.copy_global_to(guild=guild)
            # followed by syncing to the testing guild.
            await self.tree.sync(guild=guild)

        # This would also be a good place to connect to our database and
        # load anything that should be in memory prior to handling events.

    async def on_ready():
        print("Bot started")


async def main():
    """set up and run the bot"""

    load_dotenv()

    # When taking over how the bot process is run, you become responsible for a few additional things.

    # 1. logging

    # for this example, we're going to set up a rotating file logger.
    # for more info on setting up logging,
    # see https://discordpy.readthedocs.io/en/latest/logging.html and https://docs.python.org/3/howto/logging.html

    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Alternatively, you could use:
    # discord.utils.setup_logging(handler=handler, root=False)

    # One of the reasons to take over more of the process though
    # is to ensure use with other libraries or tools which also require their own cleanup.

    # Here we have a web client and a database pool, both of which do cleanup at exit.
    # We also have our bot, which depends on both of these.
    db_pass = os.environ.get("DB_PASS")
    db_user = os.environ.get("DB_USER")
    db_client = db.AsyncIOMotorClient(
        f"mongodb+srv://{db_user}:{db_pass}@cluster0.xutksl2.mongodb.net/?retryWrites=true&w=majority"
    )

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    async with await db_client.start_session() as session:
        # 2. We become responsible for starting the bot.

        exts = ["cogs.general", "cogs.music"]  # ['general', 'mod', 'dice']
        async with RoosterBot(
            commands.when_mentioned,
            db_session=session,
            initial_extensions=exts,
            testing_guild_id=int(os.environ.get("BASE_GUILD")),
            intents=intents,
        ) as bot:
            await bot.start(os.getenv("BOT_TOKEN", ""))


# For most use cases, after defining what needs to run, we can just tell asyncio to run it:
asyncio.run(main())

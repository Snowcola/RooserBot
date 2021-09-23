from pathlib import Path
from discord.ext.commands import Bot


def load_available_cogs(bot: Bot):
    print("loading cogs")
    files = [x for x in Path("./app/cogs").glob("*.py") if "__init__" not in str(x)]

    for file in files:
        cog = file.stem
        dir = str(file.parents[0]).split("/")[-1]
        print(f"Loading cog: {cog}")
        bot.load_extension(f"{dir}.{cog}")

import asyncio
import logging
import sys
import os

from discord import Intents, Game, AllowedMentions
from discord.ext import commands

# This token must exist in the environment variables for Railway.
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

# Set up logging so we will see logs in the console
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# This is how we tell Discord that we want certain data streams,
# in this case, we want to hear events related to message content
# and to member updates (e.g. when someone joins or leaves a server).
intents = Intents.default()
intents.members = True
intents.message_content = True

# Initialize the bot with various configuration options
bot = commands.Bot(
    command_prefix='!', 
    intents=intents,
    activity=Game(name="games with your heart"),  # "Playing games with your heart"
    case_insensitive=True,
    max_messages=10_000,
    allowed_mentions=AllowedMentions(everyone=False, roles=False, users=True),  # Never let the bot mention @everyone or @roles
)

async def load_extensions():
    """Load all the extensions in the /cogs folder."""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):

            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")

# Run the bot!
async def main():
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())
import aiohttp
import io
import os
import random

from aiowowapi import WowApi
from discord import File
from discord.ext import commands
from discord.ext.commands import Cog, Bot, Context


# These also need to exist in the environment variables for Railway, or we 
# can't connect to the WoW API.
BNET_CLIENT_ID = os.environ["BNET_CLIENT_ID"]
BNET_CLIENT_SECRET = os.environ["BNET_CLIENT_SECRET"]

# List of all classes and specs
CLASSES_AND_SPECS = [
    "Blood Death Knight",
    "Frost Death Knight",
    "Unholy Death Knight",
    "Havoc Demon Hunter",
    "Vengeance Demon Hunter",
    "Balance Druid",
    "Feral Druid",
    "Guardian Druid",
    "Restoration Druid",
    "Devastation Evoker",
    "Preservation Evoker",
    "Augmentation Evoker",
    "Beast Mastery Hunter",
    "Marksmanship Hunter",
    "Survival Hunter",
    "Arcane Mage",
    "Fire Mage",
    "Frost Mage",
    "Brewmaster Monk",
    "Mistweaver Monk",
    "Windwalker Monk",
    "Holy Paladin",
    "Protection Paladin",
    "Retribution Paladin",
    "Discipline Priest",
    "Holy Priest",
    "Shadow Priest",
    "Assassination Rogue",
    "Outlaw Rogue",
    "Subtlety Rogue",
    "Elemental Shaman",
    "Enhancement Shaman",
    "Restoration Shaman",
    "Affliction Warlock",
    "Demonology Warlock",
    "Destruction Warlock",
    "Arms Warrior",
    "Fury Warrior",
    "Protection Warrior"
]


class Wow(Cog):
    """Commands that leverage the WoW API."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot

    async def _get_image_from_url(self, image_url: str):
        """Use aiohttp to download a file, and return the IO stream for this file."""
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                return io.BytesIO(await response.read())

    async def _send_image(self, ctx: Context, image_path: str = None, image_url: str = None, image: io.BytesIO = None):
        """Send an image to the channel."""
        if not any([image, image_url, image_path]):
            return await ctx.send("No image provided.")
        elif sum([bool(image), bool(image_url), bool(image_path)]) > 1:
            return await ctx.send("Please only provide one image as input.")

        if image_url:
            image = await self._get_image_from_url(image_url)

        if image_path:
            image = image_path
        
        await ctx.send(file=File(image, "super_cool_image_you_guys.png"))

    async def _get_image(self, player_name: str, image_type: str, realm: str = "argent-dawn", region: str = "eu"):
        """Get a certain player image."""
        async with WowApi(BNET_CLIENT_ID, BNET_CLIENT_SECRET, region, request_debugging=True) as Client:
            images = await Client.Retail.Profile.get_character_media_summary(realm, player_name.lower())

            if image_type == "avatar":
                return images["assets"][0]["value"]
            elif image_type == "inset":
                return images["assets"][1]["value"]
            elif image_type == "main":
                return images["assets"][2]["value"]
            elif image_type == "main-raw":
                return images["assets"][3]["value"]
            
    async def _get_race(self, player_name: str, realm: str = "argent-dawn", region: str = "eu"):
        """Get the player race and gender, e.g. Male Dark Iron Dwarf"""
        async with WowApi(BNET_CLIENT_ID, BNET_CLIENT_SECRET, region, request_debugging=True) as Client:
            profile = await Client.Retail.Profile.get_character_profile_summary(realm, player_name.lower())
            race = profile["race"]["name"]
            gender = profile["gender"]["name"]

            return f"{gender} {race}"

    @commands.command()
    async def show_character(self, ctx: Context, player: str, realm: str = "argent-dawn", image_type: str = "main", region: str = "eu"):
        """Show an image of a specific WoW character."""
        image = await self._get_image(player, image_type, realm, region)
        await self._send_image(ctx, image_url=image)

    @commands.command(aliases=['new-main', "newmain", "newMain"])
    async def new_main(self, ctx: Context):
        """!new_main, !new-main, or !newMain"""
        selected_class = random.choice(CLASSES_AND_SPECS)
        
        await ctx.send(content=selected_class)



async def setup(bot: Bot) -> None:
    """
    This function is called automatically when this cog is loaded by the bot.
    It's only purpose is to load the cog above, and to pass the Bot instance into it.
    """
    await bot.add_cog(Wow(bot))

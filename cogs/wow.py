import io
import os
import random
import time

import aiohttp
from aiowowapi import WowApi
from discord import File
from discord.ext import commands
from discord.ext.commands import Cog, Bot, Context

from cogs.uwu import Uwu
from constants.warcraft import LONGCLASS_TO_SHORTCLASS 
from constants.warcraft import CLASS_SPECS_FULL 
from constants.warcraft import CLASS_ICONS
from constants.warcraft import CLASS_BREAKDOWN
from constants.warcraft import HEALERS, TANKS, MELEE, DPS, RANGED, CLASSES, CLASS_TO_SPECS

# These also need to exist in the environment variables for Railway, or we 
# can't connect to the WoW API.
BNET_CLIENT_ID = os.environ["BNET_CLIENT_ID"]
BNET_CLIENT_SECRET = os.environ["BNET_CLIENT_SECRET"]

# Constants
ALLOWED_CLASS_TYPES = (
    "ALL", "TANKS", "TANK", "HEALERS", 
    "HEALER", "DPS", "RANGED", "MELEE",
)

class Wow(Cog):
    """Commands that leverage the WoW API."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot

    async def _uwuify(self, text: str):
        """Uwuify the text."""
        return Uwu(self.bot)._uwuify(text)

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
        
    async def _get_random_class_spec(self, allowed_classes: list[str]) -> str:
        """Select and return a random class/spec, and add the correct icon string"""
        selected_class_spec = random.choice(allowed_classes)
        selected_class = CLASS_BREAKDOWN[selected_class_spec][0]
        selected_spec = CLASS_BREAKDOWN[selected_class_spec][1]
        selected_class_shortform = LONGCLASS_TO_SHORTCLASS[selected_class_spec]

        # Add a very small chance of using the treat icon instead of the class icon
        if random.randint(1, 100) <= 6:
            selected_class_icon = f"<:treat:{CLASS_ICONS['treat']}>"
            uwu_class = await self._uwuify(selected_class)
            uwu_spec = await self._uwuify(selected_spec)
            return f"{selected_class_icon}   **{uwu_spec.title()}** {uwu_class.title()}"
        
        # Otherwise, we do it all properly and shit
        else:
            selected_class_icon = f"<:{selected_class_shortform}:{CLASS_ICONS[selected_class_shortform]}>"
            return f"{selected_class_icon}   **{selected_spec}** {selected_class}"

    @commands.command()
    async def show_character(self, ctx: Context, player: str, realm: str = "argent-dawn", image_type: str = "main", region: str = "eu"):
        """Show an image of a specific WoW character."""
        image = await self._get_image(player, image_type, realm, region)
        await self._send_image(ctx, image_url=image)

    @commands.command(aliases=['new-main', "newmain"])
    async def new_main(self, ctx: Context, *, class_type: str = commands.parameter(description="A type of class in WoW, like tank or healer.", default="ALL")):
        """
        Spin the wheel and select a new random main.

        This method optionally takes one or more class types.
        
        Example:
            !new-main tank healers   # This will only return tanks and healers
            !new_main                # This may return any class
            !new_main all            # This may return any class
            !new_main dps            # This may only return DPS classes        
        """

        # Only select from classes that match the class type
        if class_type != "ALL":

            # Split it up!
            if ", " in class_type:
                list_of_specs = class_type.split(", ")
            elif "," in class_type:
                list_of_specs = class_type.split(",")
            else:
                list_of_specs = class_type.split(" ")

            # Uppercase everything
            list_of_specs = [spec.upper() for spec in list_of_specs]

            # Fix death knights and demon hunters, which will now be split.
            if "DEATH" in list_of_specs:
                list_of_specs.remove("DEATH")
                list_of_specs.remove("KNIGHT")
                list_of_specs.append("DEATH KNIGHT")

            if "DEMON" in list_of_specs:
                list_of_specs.remove("DEMON")
                list_of_specs.remove("HUNTER")
                list_of_specs.append("DEMON HUNTER")

            # Validate data
            for spec in list_of_specs:
                if spec not in ALLOWED_CLASS_TYPES and spec not in CLASSES:
                    return await ctx.send(f"❌ Invalid class type. Please provide something like 'healer', 'tank', 'ranged' or 'hunter'.")
            
            # Create a superset of allowed classes
            allowed_classes = []
            for class_type in list_of_specs:

                class_type = class_type

                if class_type in ("TANK", "HEALER"):
                    class_type += "S"

                if class_type in CLASSES:
                    allowed_classes.extend(CLASS_TO_SPECS[class_type])
                else:
                    allowed_classes.extend(globals()[class_type])

        # If the class type is ALL, just use all classes
        else:
            allowed_classes = CLASS_SPECS_FULL
        
        # Roll the classes like a slot machine!
        message = None
        rolls = random.randint(7, 14)
        for i in range(rolls):            
            new_class = await self._get_random_class_spec(allowed_classes)
            time.sleep(0.05 * (i / 1.75))
            
            # During the first iteration, send the message
            if i == 0: 
                new_class = f"🎲 {new_class}"
                message = await ctx.send(content=new_class)  # Returns a Message object

            # On the last iteration, add some celebratory stuff to show we're done
            elif i == rolls - 1:
                new_class = f"{new_class}!   🎉🎉🎉"
                await message.edit(content=new_class)


            # For all subsequent iterations, edit the message
            else:
                new_class = f"🎲 {new_class}"
                await message.edit(content=new_class)



async def setup(bot: Bot) -> None:
    """
    This function is called automatically when this cog is loaded by the bot.
    It's only purpose is to load the cog above, and to pass the Bot instance into it.
    """
    await bot.add_cog(Wow(bot))

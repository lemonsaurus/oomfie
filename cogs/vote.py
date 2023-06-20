from discord.ext import commands
from discord.ext.commands import Cog, Bot, Context

from ..constants import OFFICERS
from ..decorators import with_role


class Vote(Cog):
    """An anonymous voting system for Oomfie and the Banshees to make democratic decisions."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot

    async def _start_vote(self):
        """Start a vote among the banshees."""

    @with_role(OFFICERS)
    @commands.command()
    async def vote(self, ctx: Context):
        """
        Start a vote among the banshees.

        This will create a read-only thread in town-hall containing the vote results, updated dynamically. When
        this vote is created, it will ping @everyone so that the thread will appear in the channel list.

        Each member of the server will then be sent a DM asking for their anonymous vote. You will vote
        by pressing a button.

        Votes will be completely anonymous, and are never logged anywhere, even for technical purposes.   
        """


async def setup(bot: Bot) -> None:
    """
    This function is called automatically when this cog is loaded by the bot.
    It's only purpose is to load the cog above, and to pass the Bot instance into it.
    """
    await bot.add_cog(Vote(bot))

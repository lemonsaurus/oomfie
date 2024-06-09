from collections.abc import Callable
import contextlib
import random
import re
import typing as t
from dataclasses import dataclass
from functools import partial

import discord
from discord import Embed, Message
from discord.ext import commands
from discord.ext.commands import Cog, Context, clean_content, Bot, MessageConverter


WORD_REPLACE = {
    "small": "smol",
    "cute": "kawaii~", 
    "fluff": "floof",
    "love": "luv",
    "stupid": "baka",
    "idiot": "baka",
    "what": "nani",
    "meow": "nya~",
    "roar": "rawrr~",
}

EMOJIS = [
    "rawr x3",
    "OwO",
    "UwU",
    "o.O",
    "-.-",
    ">w<",
    "σωσ",
    "òωó",
    "ʘwʘ",
    ":3",
    "XD",
    "nyaa~~",
    "mya",
    ">_<",
    "rawr",
    "uwu",
    "^^",
    "^^;;",
]

REGEX_WORD_REPLACE = re.compile(r"(?<!w)[lr](?!w)")

REGEX_PUNCTUATION = re.compile(r"[.!?\r\n\t]")

REGEX_STUTTER = re.compile(r"(\s)([a-zA-Z])")
SUBSTITUTE_STUTTER = r"\g<1>\g<2>-\g<2>"

REGEX_NYA = re.compile(r"n([aeou][^aeiou])")
SUBSTITUTE_NYA = r"ny\1"

REGEX_EMOJI = re.compile(r"<(a)?:(\w+?):(\d{15,21}?)>", re.ASCII)


@dataclass(frozen=True, eq=True)
class Emoji:
    """Data class for an Emoji."""

    name: str
    uid: int
    animated: bool = False

    def __str__(self):
        anim_bit = "a" if self.animated else ""
        return f"<{anim_bit}:{self.name}:{self.uid}>"

    def can_display(self, bot: Bot) -> bool:
        """Determines if a bot is in a server with the emoji."""
        return bot.get_emoji(self.uid) is not None

    @classmethod
    def from_match(cls, match: tuple[str, str, str]) -> t.Optional["Emoji"]:
        """Creates an Emoji from a regex match tuple."""
        if not match or len(match) != 3 or not match[2].isdecimal():
            return None
        return cls(match[1], int(match[2]), match[0] == "a")


class Uwu(Cog):
    """Cog for the uwu command."""

    def __init__(self, bot: Bot):
        self.bot = bot

    def _suppress_links(self, message: str) -> str:
        """Accepts a message that may contain links, suppresses them, and returns them."""
        for link in set(re.findall(r"https?://[^\s]+", message, re.IGNORECASE)):
            message = message.replace(link, f"<{link}>")
        return message
    
    async def _get_discord_message(self, ctx: Context, text: str) -> Message | str:
        """
        Attempts to convert a given `text` to a discord Message object and return it.

        Conversion will succeed if given a discord Message ID or link.
        Returns `text` if the conversion fails.
        """
        with contextlib.suppress(commands.BadArgument):
            text = await MessageConverter().convert(ctx, text)
        return text
    
    async def _get_text_and_embed(self, ctx: Context, text: str) -> tuple[str, Embed | None]:
        """
        Attempts to extract the text and embed from a possible link to a discord Message.

        Does not retrieve the text and embed from the Message if it is in a channel the user does
        not have read permissions in.

        Returns a tuple of:
            str: If `text` is a valid discord Message, the contents of the message, else `text`.
            Optional[Embed]: The embed if found in the valid Message, else None
        """
        embed: Embed | None = None

        msg = await self._get_discord_message(ctx, text)
        # Ensure the user has read permissions for the channel the message is in
        if isinstance(msg, Message):
            permissions = msg.channel.permissions_for(ctx.author)
            if permissions.read_messages:
                text = msg.clean_content
                # Take first embed because we can't send multiple embeds
                if msg.embeds:
                    embed = msg.embeds[0]

        return text, embed
    
    def _convert_embed(self, func: Callable[[str, ], str], embed: Embed) -> Embed:
        """
        Converts the text in an embed using a given conversion function, then return the embed.

        Only modifies the following fields: title, description, footer, fields
        """
        embed_dict = embed.to_dict()

        embed_dict["title"] = func(embed_dict.get("title", ""))
        embed_dict["description"] = func(embed_dict.get("description", ""))

        if "footer" in embed_dict:
            embed_dict["footer"]["text"] = func(embed_dict["footer"].get("text", ""))

        if "fields" in embed_dict:
            for field in embed_dict["fields"]:
                field["name"] = func(field.get("name", ""))
                field["value"] = func(field.get("value", ""))

        return Embed.from_dict(embed_dict)

    def _word_replace(self, input_string: str) -> str:
        """Replaces words that are keys in the word replacement hash to the values specified."""
        for word, replacement in WORD_REPLACE.items():
            input_string = input_string.replace(word, replacement)
        return input_string

    def _char_replace(self, input_string: str) -> str:
        """Replace certain characters with 'w'."""
        return REGEX_WORD_REPLACE.sub("w", input_string)

    def _stutter(self, strength: float, input_string: str) -> str:
        """Adds stuttering to a string."""
        return REGEX_STUTTER.sub(partial(self._stutter_replace, strength=strength), input_string, 0)

    def _stutter_replace(self, match: re.Match, strength: float = 0.0) -> str:
        """Replaces a single character with a stuttered character."""
        match_string = match.group()
        if random.random() < strength:
            return f"{match_string}-{match_string[-1]}"  # Stutter the last character
        return match_string

    def _nyaify(self, input_string: str) -> str:
        """Nyaifies a string by adding a 'y' between an 'n' and a vowel."""
        return REGEX_NYA.sub(SUBSTITUTE_NYA, input_string, 0)

    def _emoji(self, strength: float, input_string: str) -> str:
        """Replaces some punctuation with emoticons."""
        return REGEX_PUNCTUATION.sub(partial(self._emoji_replace, strength=strength), input_string, 0)

    def _emoji_replace(self, match: re.Match, strength: float = 0.0) -> str:
        """Replaces a punctuation character with an emoticon."""
        match_string = match.group()
        if random.random() < strength:
            return f" {random.choice(EMOJIS)} "
        return match_string

    def _ext_emoji_replace(self, input_string: str) -> str:
        """Replaces any emoji the bot cannot send in input_text with a random emoticons."""
        groups = REGEX_EMOJI.findall(input_string)
        emojis = {Emoji.from_match(match) for match in groups}
        # Replace with random emoticon if unable to display
        emojis_map = {
            re.escape(str(e)): random.choice(EMOJIS)
            for e in emojis if e and not e.can_display(self.bot)
        }
        if emojis_map:
            # Pattern for all emoji markdowns to be replaced
            emojis_re = re.compile("|".join(emojis_map.keys()))
            # Replace matches with random emoticon
            return emojis_re.sub(
                lambda m: emojis_map[re.escape(m.group())],
                input_string
            )
        # Return original if no replacement
        return input_string

    def _uwuify(self, input_string: str, *, stutter_strength: float = 0.2, emoji_strength: float = 0.25) -> str:
        """Takes a string and returns an uwuified version of it."""
        input_string = input_string.lower()
        input_string = self._word_replace(input_string)
        input_string = self._nyaify(input_string)
        input_string = self._char_replace(input_string)
        input_string = self._stutter(stutter_strength, input_string)
        input_string = self._emoji(emoji_strength, input_string)
        input_string = self._ext_emoji_replace(input_string)
        return input_string

    @commands.command(name="uwu", aliases=("uwuwize", "uwuify",))
    async def uwu_command(self, ctx: Context, *, text: str | None = None) -> None:
        """
        Echo an uwuified version the passed text.

        Example:
        '.uwu Hello, my name is John' returns something like
        'hewwo, m-my name is j-john nyaa~'.
        """
        # If `text` isn't provided then we try to get message content of a replied message
        text = text or getattr(ctx.message.reference, "resolved", None)
        if isinstance(text, discord.Message):
            embeds = text.embeds
            text = text.content
        else:
            embeds = None

        if text is None:
            # If we weren't able to get the content of a replied message
            raise commands.UserInputError("Your message must have content or you must reply to a message.")

        await clean_content(fix_channel_mentions=True).convert(ctx, text)

        # Grabs the text from the embed for uwuification
        if embeds:
            embed = self._convert_embed(self._uwuify, embeds[0])
        else:
            # Parse potential message links in text
            text, embed = await self._get_text_and_embed(ctx, text)

            # If an embed is found, grab and uwuify its text
            if embed:
                embed = self._convert_embed(self._uwuify, embed)

        # Adds the text harvested from an embed to be put into another quote block.
        if text:
            converted_text = self._uwuify(text)
            converted_text = self._suppress_links(converted_text)
            converted_text = f">>> {converted_text.lstrip('> ')}"
        else:
            converted_text = None

        await ctx.send(content=converted_text, embed=embed)


async def setup(bot: Bot) -> None:
    """Load the uwu cog."""
    await bot.add_cog(Uwu(bot))
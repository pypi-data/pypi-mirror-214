from typing import Union, Annotated
from discord.ext import commands
from discord import app_commands
import discord

__all__ = (
    "AnyChannel",
    "AnyGuildChannel",
    "AnyMessageReference",
    "AnyCommand"
)

AnyGuildChannel = Union[
    discord.TextChannel,
    discord.VoiceChannel,
    discord.StageChannel,
    discord.CategoryChannel,
    discord.ForumChannel
]

AnyChannel = Union[
    discord.DMChannel,
    AnyGuildChannel
]

AnyMessageReference = Union[
    discord.Interaction,
    discord.Message,
    commands.Context
]

AnyCommand = Union[
    commands.Command,
    app_commands.Command,
    app_commands.commands.Command,
    discord.ext.commands.core.Command,
    discord.ext.commands.help._HelpCommandImpl
]
